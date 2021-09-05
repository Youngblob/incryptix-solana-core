const solanaWeb3 =  require("@solana/web3.js");
fs = require('fs');

// The state of a greeting account managed by the hello world program
// class CertificateAccount {
//   dataValue = "";
//   constructor(fields: {dataValue: string} | undefined = undefined) {
//     if (fields) {
//       this.dataValue = fields.dataValue;
//     }
//   }
// }


(async () => {

    // fs.readFile("payer_privkey", [encoding], [callback]);

    programId = process.argv[2]
    programId = new solanaWeb3.PublicKey(programId)

    studentName_storage_pubkey = process.argv[3]
    studentName_storage_pubkey = new solanaWeb3.PublicKey(studentName_storage_pubkey)

    certifyingAutority_storage_pubkey = process.argv[4]
    certifyingAutority_storage_pubkey = new solanaWeb3.PublicKey(certifyingAutority_storage_pubkey)

    isCertified_storage_pubkey = process.argv[5]
    isCertified_storage_pubkey = new solanaWeb3.PublicKey(isCertified_storage_pubkey)

    // Connect to cluster
    const connection = new solanaWeb3.Connection(
      solanaWeb3.clusterApiUrl('devnet'),
      'confirmed',
    );

    const programInfo = await connection.getAccountInfo(programId);
    console.log(programInfo.data)

    // Borsh schema definition for greeting accounts
    // const CertificateSchema = new Map([
    //   [CertificateAccount, {kind: 'struct', fields: [['dataValue', 'string']]}],
    // ]);
    //
    // const dataValue = borsh.deserialize(
    //   CertificateSchema,
    //   CertificateAccount,
    //   accountInfo.data,
    // );
    //
    // console.log(dataValue)

  })();
