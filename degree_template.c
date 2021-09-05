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

  if (params->ka_num < 1) {
    sol_log("storage account not included in the instruction");
    return ERROR_NOT_ENOUGH_ACCOUNT_KEYS;
  }

  SolAccountInfo *storageAccount_studentName = &params->ka[0];
  // The account must be owned by the program in order to modify its data
  if (!SolPubkey_same(storageAccount_studentName->owner, params->program_id)) {
    sol_log("storageAccount does not have the correct program id");
    return ERROR_INCORRECT_PROGRAM_ID;
  }

  SolAccountInfo *storageAccount_certifyingAutority = &params->ka[0];
  // The account must be owned by the program in order to modify its data
  if (!SolPubkey_same(storageAccount_certifyingAutority->owner, params->program_id)) {
    sol_log("storageAccount does not have the correct program id");
    return ERROR_INCORRECT_PROGRAM_ID;
  }

  SolAccountInfo *storageAccount_isCertified = &params->ka[1];
  // The account must be owned by the program in order to modify its data
  if (!SolPubkey_same(storageAccount_isCertified->owner, params->program_id)) {
    sol_log("storageAccount does not have the correct program id");
    return ERROR_INCORRECT_PROGRAM_ID;
  }
  // The data must be large enough to hold an uint32_t value
  // if (storageAccount->data_len < sizeof(uint32_t)) {
  //   sol_log("storageAccount data length too small to hold uint32_t value");
  //   return ERROR_INVALID_ACCOUNT_DATA;
  // }

  // struct Class class_appliedPhysics;
  // struct Class class_microcontrollers;

  char *studentName = (char *)storageAccount_studentName->data;
  // char studentName[30] = "parmu";
  char *certifyingAutority = (char *) storageAccount_certifyingAutority->data;
  // char certifyingAutority[30] = "amity";
  char *isCertified = (char *)storageAccount_isCertified->data;
  // bool isCertified = false;

  studentName = "STUDENTNAME";
  certifyingAutority = "CERTIFYINGAUTORITY";
  isCertified = "false";

  return SUCCESS;
}


extern uint64_t entrypoint(const uint8_t *input) {
  SolAccountInfo accounts[3];
  SolParameters params = (SolParameters){.ka = accounts};

  if (!sol_deserialize(input, &params, SOL_ARRAY_SIZE(accounts))) {
    return ERROR_INVALID_ARGUMENT;
  }

  // logging(&params);
  return enroll(&params);

}
