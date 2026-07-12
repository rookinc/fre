#include "fre/support_mode.hpp"

#include <limits>
#include <stdexcept>

namespace fre {
namespace {

using Wide = __int128;

std::int64_t narrow(Wide value, const char* field) {
    const Wide low = std::numeric_limits<std::int64_t>::min();
    const Wide high = std::numeric_limits<std::int64_t>::max();

    if (value < low || value > high) {
        throw std::overflow_error(field);
    }

    return static_cast<std::int64_t>(value);
}

}  // namespace

bool is_positive_support_register(const SupportRegister& h) {
    for (const std::int64_t value : h) {
        if (value <= 0) {
            return false;
        }
    }

    return true;
}

SupportModeResult evaluate_support_mode(const SupportRegister& h) {
    if (!is_positive_support_register(h)) {
        throw std::invalid_argument(
            "support coordinates must be positive integers"
        );
    }

    Wide total_wide = 0;
    for (const std::int64_t value : h) {
        total_wide += static_cast<Wide>(value);
    }

    const std::int64_t total = narrow(total_wide, "S overflow");
    SupportRegister residual6{};
    Wide k_wide = 0;

    constexpr Wide square_limit = 3037000499LL;
    const Wide output_limit =
        std::numeric_limits<std::int64_t>::max();

    for (std::size_t i = 0; i < h.size(); ++i) {
        const Wide d_wide =
            6 * static_cast<Wide>(h[i]) - total_wide;

        residual6[i] = narrow(d_wide, "d_i overflow");

        const Wide magnitude =
            d_wide < 0 ? -d_wide : d_wide;

        if (magnitude > square_limit) {
            throw std::overflow_error("K square overflow");
        }

        const Wide term = d_wide * d_wide;
        if (k_wide > output_limit - term) {
            throw std::overflow_error("K sum overflow");
        }

        k_wide += term;
    }

    const std::int64_t k_value = narrow(k_wide, "K overflow");

    return SupportModeResult{
        total,
        residual6,
        k_value,
        k_value == 0
    };
}

}  // namespace fre
