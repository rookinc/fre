#include "fre/openfhe_backend_status.hpp"

#include <iostream>

int main() {
    const fre::OpenFHEBackendStatus status =
        fre::get_openfhe_backend_status();

    std::cout
        << "{"
        << "\"backend_id\":\"" << status.backend_id << "\","
        << "\"backend_version\":\"" << status.backend_version << "\","
        << "\"install_prefix\":\"" << status.install_prefix << "\","
        << "\"available\":"
        << (status.available ? "true" : "false")
        << ",\"linked\":"
        << (status.linked ? "true" : "false")
        << ",\"profile_pinned\":"
        << (status.profile_pinned ? "true" : "false")
        << ",\"profile_admitted\":"
        << (status.profile_admitted ? "true" : "false")
        << ",\"crypto_allowed\":"
        << (status.crypto_allowed ? "true" : "false")
        << ",\"boundary\":\"" << status.boundary << "\""
        << "}\n";

    return 0;
}
