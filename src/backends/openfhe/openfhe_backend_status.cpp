#include "fre/openfhe_backend_status.hpp"

#include <openfhe.h>

#ifndef FRE_OPENFHE_PREFIX
#error "FRE_OPENFHE_PREFIX must be defined"
#endif

#ifndef FRE_OPENFHE_VERSION
#error "FRE_OPENFHE_VERSION must be defined"
#endif

namespace fre {

OpenFHEBackendStatus get_openfhe_backend_status() {
    return OpenFHEBackendStatus{
        "openfhe",
        FRE_OPENFHE_VERSION,
        FRE_OPENFHE_PREFIX,
        true,
        true,
        true,
        false,
        false,
        "link_only_profile_pinned_no_crypto"
    };
}

}  // namespace fre
