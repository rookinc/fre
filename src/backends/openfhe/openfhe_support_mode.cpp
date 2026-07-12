#include "fre/openfhe_support_mode.hpp"

#include <openfhe.h>

#include <array>
#include <stdexcept>
#include <vector>

namespace fre {
namespace {

using namespace lbcrypto;
using Ct = Ciphertext<DCRTPoly>;
using Ctx = CryptoContext<DCRTPoly>;
using Sk = PrivateKey<DCRTPoly>;

constexpr std::int64_t kModulus = 65537;
constexpr std::size_t kSlots = 8;

struct Fixture {
    const char* id;
    SupportRegister h;
};

constexpr std::array<Fixture, 4> kFixtures{{
    {"regular_uniform_10", {10, 10, 10, 10, 10, 10}},
    {"regular_uniform_20", {20, 20, 20, 20, 20, 20}},
    {"balanced_exchange_10", {11, 9, 10, 10, 10, 10}},
    {"balanced_exchange_20", {22, 18, 20, 20, 20, 20}}
}};

std::int64_t centered(std::int64_t value) {
    value %= kModulus;
    if (value > kModulus / 2) value -= kModulus;
    if (value < -(kModulus / 2)) value += kModulus;
    return value;
}

Plaintext packed(const Ctx& cc, std::int64_t value) {
    std::vector<std::int64_t> slots(kSlots, 0);
    slots[0] = value;
    return cc->MakePackedPlaintext(slots);
}

struct Decoded {
    std::int64_t first;
    bool tail_zero;
};

Decoded decode(const Ctx& cc, const Sk& key, const Ct& value) {
    Plaintext plain;
    cc->Decrypt(key, value, &plain);
    if (!plain) throw std::runtime_error("decrypt returned no plaintext");

    plain->SetLength(kSlots);
    const auto slots = plain->GetPackedValue();
    if (slots.size() < kSlots) {
        throw std::runtime_error("decrypted slot count is too small");
    }

    bool tail_zero = true;
    for (std::size_t i = 1; i < kSlots; ++i) {
        tail_zero = tail_zero && centered(slots[i]) == 0;
    }
    return {centered(slots[0]), tail_zero};
}

}  // namespace

OpenFHEBatchResult run_openfhe_support_mode_batch() {
    CCParams<CryptoContextBGVRNS> parameters;
    parameters.SetPlaintextModulus(kModulus);
    parameters.SetMultiplicativeDepth(2);
    parameters.SetSecurityLevel(HEStd_NotSet);
    parameters.SetRingDim(1024);
    parameters.SetBatchSize(kSlots);

    const auto cc = GenCryptoContext(parameters);
    cc->Enable(PKE);
    cc->Enable(LEVELEDSHE);

    const auto keys = cc->KeyGen();
    if (!keys.good()) throw std::runtime_error("KeyGen failed");
    cc->EvalMultKeyGen(keys.secretKey);

    OpenFHEBatchResult batch{
        "fre.support_mode.openfhe.batch.001",
        "fre.support_mode.openfhe_execution_gate.v0.1",
        "fre.openfhe.bgv.evalmult.executed.v0.1",
        true, true, true, true, {}, true, true, false
    };

    for (const auto& fixture : kFixtures) {
        std::array<Ct, kSupportCoordinateCount> encrypted{};
        for (std::size_t i = 0; i < encrypted.size(); ++i) {
            encrypted[i] = cc->Encrypt(
                keys.publicKey, packed(cc, fixture.h[i])
            );
        }
        const Ct minus_one = cc->Encrypt(
            keys.publicKey, packed(cc, -1)
        );

        Ct sum = encrypted[0];
        for (std::size_t i = 1; i < encrypted.size(); ++i) {
            sum = cc->EvalAdd(sum, encrypted[i]);
        }

        const Ct negative_sum = cc->EvalMult(sum, minus_one);
        std::array<Ct, kSupportCoordinateCount> residual{};
        std::array<Ct, kSupportCoordinateCount> squared{};

        for (std::size_t i = 0; i < encrypted.size(); ++i) {
            Ct six_h = encrypted[i];
            for (int copy = 1; copy < 6; ++copy) {
                six_h = cc->EvalAdd(six_h, encrypted[i]);
            }
            residual[i] = cc->EvalAdd(six_h, negative_sum);
            squared[i] = cc->EvalMult(residual[i], residual[i]);
        }

        Ct k_cipher = squared[0];
        for (std::size_t i = 1; i < squared.size(); ++i) {
            k_cipher = cc->EvalAdd(k_cipher, squared[i]);
        }

        const auto reference = evaluate_support_mode(fixture.h);
        const auto observed_sum = decode(cc, keys.secretKey, sum);
        SupportRegister observed_d{};
        bool tails_zero = observed_sum.tail_zero;

        for (std::size_t i = 0; i < residual.size(); ++i) {
            const auto value = decode(cc, keys.secretKey, residual[i]);
            observed_d[i] = value.first;
            tails_zero = tails_zero && value.tail_zero;
        }

        const auto observed_k = decode(
            cc, keys.secretKey, k_cipher
        );
        tails_zero = tails_zero && observed_k.tail_zero;

        const bool match =
            observed_sum.first == reference.S
            && observed_d == reference.d
            && observed_k.first == reference.K;

        batch.fixtures.push_back(OpenFHEFixtureResult{
            fixture.id,
            observed_sum.first,
            observed_d,
            observed_k.first,
            observed_k.first == 0,
            tails_zero,
            tails_zero,
            match
        });
        batch.all_reference_match =
            batch.all_reference_match && match;
        batch.all_slot_tails_zero =
            batch.all_slot_tails_zero && tails_zero;
    }

    return batch;
}

}  // namespace fre
