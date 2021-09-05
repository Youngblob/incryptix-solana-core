const solanaWeb3 =  require("@solana/web3.js");
fs = require('fs');

(async () => {

    // fs.readFile("payer_privkey", [encoding], [callback]);

    programId = process.argv[2]
    programId = new solanaWeb3.PublicKey(programId)
    SEED = "nuiawecniludfcnzlsdj"+Math.floor(Math.random() * (10000))
    SIZE = 32

    // Connect to cluster
    const connection = new solanaWeb3.Connection(
      solanaWeb3.clusterApiUrl('devnet'),
      'confirmed',
    );

    // read this from file instead
    privkey = [102,234,72,112,223,198,208,42,253,226,78,218,1,203,179,163,34,119,15,134,156,108,127,75,81,230,223,210,5,176,126,27,109,168,98,200,150,209,164,73,170,164,49,153,68,219,78,204,215,139,100,83,231,204,141,144,65,247,80,199,208,157,38,217]
    const payerAccount = new solanaWeb3.Account(privkey);

    const lamports = await connection.getMinimumBalanceForRentExemption(SIZE);
    // derive a public key
    const storageAccount_Pubkey = await solanaWeb3.PublicKey.createWithSeed(
      payerAccount.publicKey,
      SEED,
      programId,
    );

    const transaction = new solanaWeb3.Transaction().add(
      solanaWeb3.SystemProgram.createAccountWithSeed({
          fromPubkey: payerAccount.publicKey,
          basePubkey: payerAccount.publicKey,
          seed: SEED,
          newAccountPubkey: storageAccount_Pubkey,
          lamports,
          space: SIZE,
          programId,
      }),
    );
    const hash = await solanaWeb3.sendAndConfirmTransaction(connection, transaction, [payerAccount])
    console.log(storageAccount_Pubkey.toString())
  })();
