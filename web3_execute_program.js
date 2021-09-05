const solanaWeb3 =  require("@solana/web3.js");
fs = require('fs');

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

    // read this from file instead
    privkey = [102,234,72,112,223,198,208,42,253,226,78,218,1,203,179,163,34,119,15,134,156,108,127,75,81,230,223,210,5,176,126,27,109,168,98,200,150,209,164,73,170,164,49,153,68,219,78,204,215,139,100,83,231,204,141,144,65,247,80,199,208,157,38,217]
    const payerAccount = new solanaWeb3.Account(privkey);

    storageAccounts = [
      {
        pubkey: studentName_storage_pubkey,
        isSigner: false,
        isWritable: true
      },
      {
        pubkey: certifyingAutority_storage_pubkey,
        isSigner: false,
        isWritable: true
      },
      {
        pubkey: isCertified_storage_pubkey,
        isSigner: false,
        isWritable: true
      }
    ]

    const instruction = new solanaWeb3.TransactionInstruction({
      keys: storageAccounts,
      programId: programId,
      data: Buffer.alloc(0), // All instructions are hellos
    });

    const hash = await solanaWeb3.sendAndConfirmTransaction(
      connection,
      new solanaWeb3.Transaction().add(instruction),
      [payerAccount]
    );

    console.log(hash)
  })();
