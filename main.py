// 游戏数据存储键
const GAME_DATA_KEY = "rpg_game_data";

// 默认用户数据结构
const DEFAULT_USER_DATA = {
    lastCheckin: null,
    money: 0,
    todoList: [],
    winCount: 0,
    loseCount: 0,
    drawCount: 0,
};

// 获取用户数据
async function getUserData(userId) {
    let gameData = await astrbot.storage.get(GAME_DATA_KEY) || {};
    if (!gameData[userId]) {
        gameData[userId] = { ...DEFAULT_USER_DATA };
    }
    return gameData[userId];
}

// 保存用户数据
async function saveUserData(userId, userData) {
    let gameData = await astrbot.storage.get(GAME_DATA_KEY) || {};
    gameData[userId] = userData;
    await astrbot.storage.set(GAME_DATA_KEY, gameData);
}

// 签到功能
async function handleCheckin(userId) {
    const userData = await getUserData(userId);
    const now = new Date();
    const today = now.toDateString();

    if (userData.lastCheckin === today) {
        return "你今天已经签到过了！";
    }

    userData.lastCheckin = today;
    userData.money += 10;
    await saveUserData(userId, userData);
    return "签到成功！你获得了 10 金币。";
}

// 打劫功能
async function handleRob(userId) {
    const userData = await getUserData(userId);
    const robChance = Math.random();
    if (robChance > 0.7) {
        const amount = Math.floor(Math.random() * 20) + 1;
        userData.money += amount;
        await saveUserData(userId, userData);
        return `打劫成功！你获得了 ${amount} 金币。`;
    } else {
        const amount = Math.floor(Math.random() * 10) + 1;
        userData.money = Math.max(0, userData.money - amount);
        await saveUserData(userId, userData);
        return `打劫失败！你被抓了，损失了 ${amount} 金币。`;
    }
}

// 打工功能
async function handleWork(userId) {
    const userData = await getUserData(userId);
    const amount = Math.floor(Math.random() * 30) + 10;
    userData.money += amount;
    await saveUserData(userId, userData);

    return `打工结束，你获得了 ${amount} 金币`;
}


// 猜拳功能
async function handleRockPaperScissors(userId, userChoice) {
    const userData = await getUserData(userId)
    const choices = ["石头", "剪刀", "布"];
    const botChoice = choices[Math.floor(Math.random() * 3)];

    if (!choices.includes(userChoice)) {
        return "请输入 '石头'，'剪刀' 或 '布'。";
    }

    let resultMessage;
    if (userChoice === botChoice) {
        resultMessage = `你出了 ${userChoice}，我出了 ${botChoice}，平局！`;
        userData.drawCount++;
    } else if (
        (userChoice === "石头" && botChoice === "剪刀") ||
        (userChoice === "剪刀" && botChoice === "布") ||
        (userChoice === "布" && botChoice === "石头")
    ) {
        resultMessage = `你出了 ${userChoice}，我出了 ${botChoice}，你赢了！`;
        userData.winCount++;
        userData.money += 5; // 赢了奖励5金币
    } else {
        resultMessage = `你出了 ${userChoice}，我出了 ${botChoice}，你输了！`;
        userData.loseCount++;
        userData.money = Math.max(0, userData.money - 2); // 输了扣2金币
    }
    await saveUserData(userId, userData);
    return resultMessage + `\n你目前的战绩为： 赢:${userData.winCount}  输:${userData.loseCount}  平:${userData.drawCount}`;
}

// 添加代办事项
async function handleAddTodo(userId, task) {
    const userData = await getUserData(userId);
    userData.todoList.push(task);
    await saveUserData(userId, userData);
    return `添加代办事项：${task}`;
}

// 查看代办事项
async function handleViewTodos(userId) {
    const userData = await getUserData(userId);
    if (userData.todoList.length === 0) {
        return "你没有待办事项。";
    }
    return "你的待办事项：\n" + userData.todoList.map((task, index) => `${index + 1}. ${task}`).join("\n");
}

// 删除代办事项
async function handleRemoveTodo(userId, index) {
    const userData = await getUserData(userId);
    if (index < 1 || index > userData.todoList.length) {
        return "无效的待办事项索引。";
    }
    const removedTask = userData.todoList.splice(index - 1, 1)[0];
    await saveUserData(userId, userData);
    return `删除了待办事项：${removedTask}`;
}

// 处理消息
astrbot.onmessage(async (message) => {
    const content = message.content;
    const userId = message.author.id;

    if (content.startsWith("/签到")) {
        const response = await handleCheckin(userId);
        astrbot.send(response, message.channel_id);
    } else if (content.startsWith("/打劫")) {
        const response = await handleRob(userId);
        astrbot.send(response, message.channel_id);
    } else if (content.startsWith("/打工")) {
        const response = await handleWork(userId);
        astrbot.send(response, message.channel_id);
    }
     else if (content.startsWith("/猜拳")) {
        const userChoice = content.substring(4).trim();
        const response = await handleRockPaperScissors(userId, userChoice);
        astrbot.send(response, message.channel_id);
    } else if (content.startsWith("/添加代办")) {
        const task = content.substring(5).trim();
        if (task) {
            const response = await handleAddTodo(userId, task);
            astrbot.send(response, message.channel_id);
        } else {
            astrbot.send("请提供要添加的待办事项。", message.channel_id);
        }
    } else if (content.startsWith("/查看代办")) {
        const response = await handleViewTodos(userId);
        astrbot.send(response, message.channel_id);
    } else if (content.startsWith("/删除代办")) {
        const index = parseInt(content.substring(5).trim());
        if (!isNaN(index)) {
            const response = await handleRemoveTodo(userId, index);
            astrbot.send(response, message.channel_id);
        } else {
            astrbot.send("请提供要删除的待办事项索引。", message.channel_id);
        }
    }
});

