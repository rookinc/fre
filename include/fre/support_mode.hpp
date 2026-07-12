#pragma once

#include <array>
#include <cstddef>
#include <cstdint>

namespace fre {

inline constexpr std::size_t kSupportCoordinateCount = 6;

using SupportRegister =
    std::array<std::int64_t, kSupportCoordinateCount>;

struct SupportModeResult {
    std::int64_t S;
    SupportRegister d;
    std::int64_t K;
    bool regular;
};

bool is_positive_support_register(const SupportRegister& h);

SupportModeResult evaluate_support_mode(const SupportRegister& h);

}  // namespace fre
