#include "fre/openfhe_support_mode.hpp"

#include <exception>
#include <iostream>

namespace {

const char* boolean(bool value) {
    return value ? "true" : "false";
}

void print_result(const fre::OpenFHEBatchResult& batch) {
    std::cout
        << "{"
        << "\"run_id\":\"" << batch.run_id << "\","
        << "\"gate_id\":\"" << batch.gate_id << "\","
        << "\"profile_id\":\"" << batch.profile_id << "\","
        << "\"gate_admitted\":" << boolean(batch.gate_admitted)
        << ",\"context_generated\":" << boolean(batch.context_generated)
        << ",\"key_generated\":" << boolean(batch.key_generated)
        << ",\"eval_mult_key_generated\":"
        << boolean(batch.eval_mult_key_generated)
        << ",\"fixtures\":[";

    for (std::size_t row = 0; row < batch.fixtures.size(); ++row) {
        if (row != 0) std::cout << ",";
        const auto& fixture = batch.fixtures[row];

        std::cout
            << "{"
            << "\"fixture_id\":\"" << fixture.fixture_id << "\","
            << "\"S\":" << fixture.S
            << ",\"d\":[";

        for (std::size_t i = 0; i < fixture.d.size(); ++i) {
            if (i != 0) std::cout << ",";
            std::cout << fixture.d[i];
        }

        std::cout
            << "],\"K\":" << fixture.K
            << ",\"regular\":" << boolean(fixture.regular)
            << ",\"slot_tail_zero\":"
            << boolean(fixture.slot_tail_zero)
            << ",\"decrypt_verified\":"
            << boolean(fixture.decrypt_verified)
            << ",\"reference_match\":"
            << boolean(fixture.reference_match)
            << "}";
    }

    std::cout
        << "],\"all_reference_match\":"
        << boolean(batch.all_reference_match)
        << ",\"all_slot_tails_zero\":"
        << boolean(batch.all_slot_tails_zero)
        << ",\"private_material_committed\":"
        << boolean(batch.private_material_committed)
        << "}\n";
}

}  // namespace

int main() {
    try {
        const auto batch = fre::run_openfhe_support_mode_batch();
        print_result(batch);

        return (
            batch.gate_admitted
            && batch.all_reference_match
            && batch.all_slot_tails_zero
            && !batch.private_material_committed
        ) ? 0 : 1;
    } catch (const std::exception& exc) {
        std::cerr
            << "ERROR openfhe_support_mode_smoke_failed: "
            << exc.what()
            << "\n";
        return 2;
    }
}
