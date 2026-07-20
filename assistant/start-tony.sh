#!/bin/bash
cd "/Users/vovanduc/Code/dcnet/flow_next/assistant"

# Update main clawdbot với Tony token tạm thời
clawdbot config set channels.telegram.default.token "8274808645:AAEbJeYyz4ciJZBCB_BE2hB6KMQxrbs0ubs"

# Restart gateway với workspace Tony
CLAWDBOT_WORKSPACE="/Users/vovanduc/Code/dcnet/flow_next/assistant" clawdbot gateway restart

echo "Tony bot started with workspace: /Users/vovanduc/Code/dcnet/flow_next/assistant"
echo "Bot: @DcnetTonyBot"
echo "Test: Message the bot directly first"