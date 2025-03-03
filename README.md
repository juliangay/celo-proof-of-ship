# Celo Proof of Ship Agent

## Mission
Proof of Ship Agent is designed to track, recognize, and reward contributors in the Celo builder community participating in the Proof of Ship buildathon. The project leverages blockchain technology and AI-powered automation to streamline project submissions, progress tracking, and rewards distribution.

## Objectives
- **Provide a transparent tracking system** for buildathon progress and contributions.
- **Enable easy submission and review** of Proof of Ship projects.
- **Recognize contributors** by minting Soulbound NFTs for verified submissions.
- **Distribute rewards seamlessly** via a SAFE wallet mechanism.
- **Automate publication and engagement** through AI-powered agents for Farcaster and Twitter.

## Architecture Overview
### **Dashboard**
A **Streamlit-based application** that allows contributors to:
- Submit their Proof of Ship contributions.
- Track project progress and view submission history.
- Judges can review and approve submissions efficiently.

### **Agents**
AI-powered automation for various tasks:
- **Blockchain Agent:** A Python application leveraging the Celo SDK to interact with the blockchain.
- **Submission Review Agent:** A Replit-based agent that assists judges in reviewing submissions and distributing rewards.
- **Submission Assistance Agent:** A Replit-based agent that guides contributors through the Proof of Ship submission process.
- **Publication Agent:** A Replit-based agent that helps contributors share their submissions on **Farcaster and Twitter**.

## Smart Contract Integration
Proof of Ship leverages smart contracts to mint **Soulbound NFTs**, ensuring verified contributions receive recognition. The project also tracks contract deployments and submission activity via blockchain.

### **Deployed Contract Addresses on Celo**
#### Soulbound Token Contract Address on Celo Alfajores Testnet:
`0x3ac1eb269df27294e8e3e68f0c699480f4f6b8ba`

## Key Features
✅ **GitHub Submission Tracking** - Verify and track public repository submissions.
✅ **Smart Contract Monitoring** - Record deployment activity on Celo Mainnet & Alfajores.
✅ **Social Verification** - Monitor Farcaster cast activity related to Proof of Ship.
✅ **Soulbound NFT Minting** - Reward verified contributors with immutable NFTs.
✅ **Automated Reward Distribution** - Distribute incentives to eligible addresses via SAFE wallet.

## Getting Started
### **1. Clone the Repository**
```sh
 git clone https://github.com/juliangay/celo-proof-of-ship.git
 cd celo-proof-of-ship
```

### **2. Install Dependencies**
Ensure you have Python and necessary dependencies installed:
```sh
pip install -r requirements.txt
```

### **3. Run the Streamlit Dashboard**
```sh
streamlit run app.py
```

### **4. Deploy and Test Smart Contracts**
Deploy smart contracts to Celo Testnet using Hardhat:
```sh
npx hardhat run scripts/deploy.js --network alfajores
```

## Contribution Guidelines
1. **Fork the repository** and create a new branch.
2. **Work on your feature/fix** and commit changes.
3. **Submit a pull request** for review.
4. **Engage with the community** on Farcaster and Twitter.

## License
This project is open-source and available under the [MIT License](LICENSE).

## Contact & Community
- Follow updates on **[Farcaster](https://www.farcaster.xyz/)**
- Connect on **[Twitter](https://twitter.com/yourprofile)**
- Join discussions on **Celo Discord**

Let's build the future of decentralized contributions together! 🚀
