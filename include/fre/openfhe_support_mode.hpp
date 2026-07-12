#pragma once

#include "fre/support_mode.hpp"

#include <cstdint>
#include <string>
#include <vector>

namespace fre {

struct OpenFHEFixtureResult {
    std::string fixture_id;
    std::int64_t S;
    SupportRegister d;
    std::int64_t K;
    bool regular;
    bool slot_tail_zero;
    bool decrypt_verified;
    bool reference_match;
};

struct OpenFHEBatchResult {
    std::string run_id;
    std::string gate_id;
    std::string profile_id;
    bool gate_admitted;
    bool context_generated;
    bool key_generated;
    bool eval_mult_key_generated;
    std::vector<OpenFHEFixtureResult> fixtures;
    bool all_reference_match;
    bool all_slot_tails_zero;
    bool private_material_committed;
};

OpenFHEBatchResult run_openfhe_support_mode_batch();

}  // namespace fre
