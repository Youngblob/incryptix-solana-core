/**
 * @brief A program demonstrating logging
 */
#include <solana_sdk.h>

extern void logging(SolParameters *params) {
  // Log a string
  sol_log("static string");

  // Log a slice
  sol_log_array(params->data, params->data_len);

  // Log a public key
  sol_log_pubkey(params->program_id);

  // Log all the program's input parameters
  sol_log_params(params);

  // Log the number of compute units remaining that the program can consume.
  sol_log_compute_units();

}

// struct Class {
//   char title[30];
//   _bool isCompleted;
// }

extern uint64_t enroll(SolParameters *params){

  sol_log("Request received to enroll in degree");

  // char studentName[] = params->data[1];
  SolAccountInfo *sourceAddress = &params->ka[0];

  // struct Class class_appliedPhysics;
  // struct Class class_microcontrollers;

  char studentName[30] = "STUDENTNAME";
  char certifyingAutority[30] = "CERTIFYINGAUTORITY";
  bool isCertified = false;

  return SUCCESS;
}


extern uint64_t entrypoint(const uint8_t *input) {
  SolAccountInfo accounts[1];
  SolParameters params = (SolParameters){.ka = accounts};

  if (!sol_deserialize(input, &params, SOL_ARRAY_SIZE(accounts))) {
    return ERROR_INVALID_ARGUMENT;
  }

  logging(&params);
  return enroll(&params);

}
