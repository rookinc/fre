#include "fre/support_mode.hpp"

#include <charconv>
#include <cstdint>
#include <exception>
#include <iostream>
#include <string_view>
#include <system_error>

namespace {

bool parse_integer(
    std::string_view text,
    std::int64_t& value
) {
    const char* first = text.data();
    const char* last = text.data() + text.size();

    const auto parsed = std::from_chars(first, last, value);

    return parsed.ec == std::errc{} && parsed.ptr == last;
}

void print_result(const fre::SupportModeResult& result) {
    std::cout
        << "{"
        << "\"pipeline_id\":\"support_mode_reference_v0.1\","
        << "\"source_class\":\"six_support_register\","
        << "\"S\":" << result.S
        << ",\"d\":[";

    for (std::size_t i = 0; i < result.d.size(); ++i) {
        if (i != 0) {
            std::cout << ",";
        }
        std::cout << result.d[i];
    }

    std::cout
        << "],\"K\":" << result.K
        << ",\"regular\":"
        << (result.regular ? "true" : "false")
        << "}\n";
}

}  // namespace

int main(int argc, char** argv) {
    constexpr int expected_argument_count =
        static_cast<int>(fre::kSupportCoordinateCount) + 1;

    if (argc != expected_argument_count) {
        std::cerr
            << "ERROR expected exactly six support coordinates\n";
        return 2;
    }

    fre::SupportRegister h{};

    for (std::size_t i = 0; i < h.size(); ++i) {
        const std::string_view text(argv[i + 1]);

        if (!parse_integer(text, h[i])) {
            std::cerr
                << "ERROR invalid integer at coordinate "
                << (i + 1)
                << "\n";
            return 2;
        }
    }

    try {
        const fre::SupportModeResult result =
            fre::evaluate_support_mode(h);

        print_result(result);
        return 0;
    } catch (const std::exception& exc) {
        std::cerr
            << "ERROR reference_evaluation_failed: "
            << exc.what()
            << "\n";
        return 3;
    }
}
