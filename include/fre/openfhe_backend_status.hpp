#pragma once

#include <string>

namespace fre {

struct OpenFHEBackendStatus {
    std::string backend_id;
    std::string backend_version;
    std::string install_prefix;
    bool available;
    bool linked;
    bool profile_pinned;
    bool profile_admitted;
    bool crypto_allowed;
    std::string boundary;
};

OpenFHEBackendStatus get_openfhe_backend_status();

}  // namespace fre
