#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
坦克大战 HTML 游戏生成器
运行此脚本将生成一个完整的 HTML5 坦克大战游戏文件
"""

import os
import webbrowser

HTML_CONTENT = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>坦克大战 HTML5</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            background: #1a1a1a;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            font-family: 'Microsoft YaHei', sans-serif;
            overflow: hidden;
        }
        #gameContainer {
            text-align: center;
        }
        #gameCanvas {
            border: 3px solid #4a4a4a;
            background: #000;
            display: block;
            margin: 0 auto;
        }
        #info {
            color: #fff;
            margin-top: 10px;
            font-size: 16px;
        }
        #score {
            color: #ffcc00;
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        #controls {
            color: #aaa;
            margin-top: 10px;
            font-size: 14px;
        }
        #gameOver {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.9);
            padding: 30px 50px;
            border-radius: 10px;
            border: 2px solid #ff0000;
            display: none;
            text-align: center;
        }
        #gameOver h2 {
            color: #ff0000;
            font-size: 36px;
            margin-bottom: 20px;
        }
        #gameOver p {
            color: #fff;
            font-size: 18px;
            margin-bottom: 20px;
        }
        #restartBtn {
            background: #ff0000;
            color: #fff;
            border: none;
            padding: 10px 30px;
            font-size: 18px;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.3s;
        }
        #restartBtn:hover {
            background: #cc0000;
        }
        #startScreen {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.9);
            padding: 40px 60px;
            border-radius: 10px;
            border: 2px solid #00ff00;
            text-align: center;
        }
        #startScreen h1 {
            color: #00ff00;
            font-size: 42px;
            margin-bottom: 20px;
            text-shadow: 0 0 10px #00ff00;
        }
        #startScreen p {
            color: #fff;
            font-size: 16px;
            margin: 10px 0;
        }
        #startBtn {
            background: #00ff00;
            color: #000;
            border: none;
            padding: 12px 40px;
            font-size: 20px;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 20px;
            font-weight: bold;
            transition: background 0.3s;
        }
        #startBtn:hover {
            background: #00cc00;
        }
    </style>
</head>
<body>
    <div id="gameContainer">
        <div id="score">得分: 0 | 生命: ❤❤❤</div>
        <canvas id="gameCanvas" width="780" height="580"></canvas>
        <div id="controls">
            方向键移动 | 空格键射击
        </div>
    </div>

    <div id="startScreen">
        <h1>🎮 坦克大战</h1>
        <p>消灭所有敌方坦克，保护你的基地！</p>
        <p>每消灭一个敌人得 100 分</p>
        <p>方向键 ↑↓←→ 移动坦克</p>
        <p>空格键 发射炮弹</p>
        <button id="startBtn">开始游戏</button>
    </div>

    <div id="gameOver">
        <h2>游戏结束</h2>
        <p id="finalScore">最终得分: 0</p>
        <button id="restartBtn">重新开始</button>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        const CELL_SIZE = 26;
        const COLS = 30;
        const ROWS = 22;

        // 游戏状态
        let gameRunning = false;
        let score = 0;
        let playerLives = 3;
        let enemies = [];
        let bullets = [];
        let particles = [];
        let walls = [];
        let player = null;
        let enemySpawnTimer = 0;
        let enemySpawnInterval = 180;
        let maxEnemies = 5;

        // 方向常量
        const UP = 0, RIGHT = 1, DOWN = 2, LEFT = 3;

        // 关卡地图 (0=空地, 1=砖墙, 2=钢墙, 3=基地)
        const mapData = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0],
            [0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0],
            [0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0],
            [0,0,1,1,0,0,1,1,0,0,1,1,2,2,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0],
            [0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0],
            [0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,1,1,0,0,1,1,0,0,1,1,2,2,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0],
            [0,0,1,1,0,0,1,1,0,0,1,1,2,2,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ];

        // 键盘输入
        const keys = {};
        document.addEventListener('keydown', (e) => {
            keys[e.key] = true;
            if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', ' '].includes(e.key)) {
                e.preventDefault();
            }
        });
        document.addEventListener('keyup', (e) => {
            keys[e.key] = false;
        });

        // 矩形碰撞检测
        function rectCollision(r1, r2) {
            return r1.x < r2.x + r2.width &&
                   r1.x + r1.width > r2.x &&
                   r1.y < r2.y + r2.height &&
                   r1.y + r1.height > r2.y;
        }

        // 坦克类
        class Tank {
            constructor(x, y, type, direction = UP) {
                this.x = x;
                this.y = y;
                this.width = 24;
                this.height = 24;
                this.type = type; // 'player' 或 'enemy'
                this.direction = direction;
                this.speed = type === 'player' ? 1.2 : 1.0;
                this.color = type === 'player' ? '#00ff00' : '#ff0000';
                this.moveTimer = 0;
                this.shootTimer = 0;
                this.shootInterval = type === 'player' ? 15 : 90 + Math.random() * 60;
                this.alive = true;
                this.flashTimer = 0;
            }

            update() {
                if (!this.alive) return;
                this.flashTimer = Math.max(0, this.flashTimer - 1);
                this.shootTimer++;

                if (this.type === 'player') {
                    this.handlePlayerInput();
                } else {
                    this.handleAI();
                }
            }

            handlePlayerInput() {
                let dx = 0, dy = 0;
                if (keys['ArrowUp']) { dy = -this.speed; this.direction = UP; }
                else if (keys['ArrowDown']) { dy = this.speed; this.direction = DOWN; }
                else if (keys['ArrowLeft']) { dx = -this.speed; this.direction = LEFT; }
                else if (keys['ArrowRight']) { dx = this.speed; this.direction = RIGHT; }

                if (dx !== 0 || dy !== 0) {
                    this.move(dx, dy);
                }

                if (keys[' '] && this.shootTimer >= this.shootInterval) {
                    this.shoot();
                    this.shootTimer = 0;
                }
            }

            handleAI() {
                this.moveTimer++;
                if (this.moveTimer > 30 + Math.random() * 60) {
                    this.direction = Math.floor(Math.random() * 4);
                    this.moveTimer = 0;
                }

                let dx = 0, dy = 0;
                switch (this.direction) {
                    case UP: dy = -this.speed; break;
                    case DOWN: dy = this.speed; break;
                    case LEFT: dx = -this.speed; break;
                    case RIGHT: dx = this.speed; break;
                }
                this.move(dx, dy);

                if (this.shootTimer >= this.shootInterval) {
                    this.shoot();
                    this.shootTimer = 0;
                }
            }

            move(dx, dy) {
                const newX = this.x + dx;
                const newY = this.y + dy;

                // 边界检测
                if (newX < 0 || newX + this.width > canvas.width ||
                    newY < 0 || newY + this.height > canvas.height) {
                    return;
                }

                // 墙壁碰撞检测
                const newRect = { x: newX, y: newY, width: this.width, height: this.height };
                for (let wall of walls) {
                    if (wall.type !== 0 && rectCollision(newRect, wall)) {
                        if (this.type === 'enemy') {
                            this.direction = Math.floor(Math.random() * 4);
                        }
                        return;
                    }
                }

                // 坦克间碰撞检测
                for (let tank of [...enemies, player]) {
                    if (tank !== this && tank.alive && rectCollision(newRect, tank)) {
                        if (this.type === 'enemy') {
                            this.direction = Math.floor(Math.random() * 4);
                        }
                        return;
                    }
                }

                this.x = newX;
                this.y = newY;
            }

            shoot() {
                let bx = this.x + this.width / 2 - 3;
                let by = this.y + this.height / 2 - 3;
                let bdx = 0, bdy = 0;
                const speed = 4;

                switch (this.direction) {
                    case UP: bdy = -speed; by = this.y - 6; break;
                    case DOWN: bdy = speed; by = this.y + this.height; break;
                    case LEFT: bdx = -speed; bx = this.x - 6; break;
                    case RIGHT: bdx = speed; bx = this.x + this.width; break;
                }

                bullets.push(new Bullet(bx, by, bdx, bdy, this.type));
            }

            draw() {
                if (!this.alive) return;
                
                ctx.save();
                if (this.flashTimer > 0 && Math.floor(this.flashTimer / 3) % 2 === 0) {
                    ctx.globalAlpha = 0.5;
                }

                const cx = this.x + this.width / 2;
                const cy = this.y + this.height / 2;
                ctx.translate(cx, cy);
                ctx.rotate(this.direction * Math.PI / 2);
                ctx.translate(-cx, -cy);

                // 坦克身体
                ctx.fillStyle = this.color;
                ctx.fillRect(this.x + 2, this.y + 2, this.width - 4, this.height - 4);
                
                // 坦克履带
                ctx.fillStyle = '#333';
                ctx.fillRect(this.x, this.y, 4, this.height);
                ctx.fillRect(this.x + this.width - 4, this.y, 4, this.height);
                
                // 炮塔
                ctx.fillStyle = this.type === 'player' ? '#00cc00' : '#cc0000';
                ctx.fillRect(this.x + 8, this.y + 8, 8, 8);
                
                // 炮管
                ctx.fillStyle = '#666';
                ctx.fillRect(this.x + 10, this.y - 8, 4, 14);

                ctx.restore();
            }

            hit() {
                this.flashTimer = 20;
                createExplosion(this.x + this.width/2, this.y + this.height/2, this.color);
            }
        }

        // 子弹类
        class Bullet {
            constructor(x, y, dx, dy, owner) {
                this.x = x;
                this.y = y;
                this.width = 6;
                this.height = 6;
                this.dx = dx;
                this.dy = dy;
                this.owner = owner;
                this.alive = true;
            }

            update() {
                this.x += this.dx;
                this.y += this.dy;

                // 边界检测
                if (this.x < 0 || this.x > canvas.width || this.y < 0 || this.y > canvas.height) {
                    this.alive = false;
                    return;
                }

                // 墙壁碰撞
                const bRect = { x: this.x, y: this.y, width: this.width, height: this.height };
                for (let i = walls.length - 1; i >= 0; i--) {
                    if (walls[i].type !== 0 && rectCollision(bRect, walls[i])) {
                        if (walls[i].type === 1) { // 砖墙可被摧毁
                            createExplosion(walls[i].x + walls[i].width/2, walls[i].y + walls[i].height/2, '#cc6633');
                            walls[i].type = 0;
                        } else if (walls[i].type === 3) { // 基地被击中
                            createExplosion(walls[i].x + walls[i].width/2, walls[i].y + walls[i].height/2, '#ffcc00');
                            gameOver();
                            return;
                        } else {
                            createExplosion(this.x + this.width/2, this.y + this.height/2, '#888');
                        }
                        this.alive = false;
                        return;
                    }
                }

                // 坦克碰撞
                const targets = this.owner === 'player' ? enemies : [player];
                for (let target of targets) {
                    if (target.alive && rectCollision(bRect, target)) {
                        this.alive = false;
                        target.hit();
                        
                        if (this.owner === 'player') {
                            target.alive = false;
                            score += 100;
                            updateScore();
                            createExplosion(target.x + target.width/2, target.y + target.height/2, '#ff6600');
                        } else {
                            playerLives--;
                            updateScore();
                            if (playerLives <= 0) {
                                target.alive = false;
                                gameOver();
                            } else {
                                setTimeout(() => {
                                    if (gameRunning) {
                                        player.x = 100;
                                        player.y = 500;
                                        player.direction = UP;
                                        player.flashTimer = 60;
                                    }
                                }, 1000);
                            }
                        }
                        return;
                    }
                }
            }

            draw() {
                ctx.fillStyle = this.owner === 'player' ? '#ffff00' : '#ff6600';
                ctx.fillRect(this.x, this.y, this.width, this.height);
            }
        }

        // 粒子效果
        class Particle {
            constructor(x, y, color) {
                this.x = x;
                this.y = y;
                this.vx = (Math.random() - 0.5) * 6;
                this.vy = (Math.random() - 0.5) * 6;
                this.life = 30;
                this.color = color;
                this.size = 3 + Math.random() * 4;
            }

            update() {
                this.x += this.vx;
                this.y += this.vy;
                this.life--;
                this.size *= 0.95;
            }

            draw() {
                ctx.fillStyle = this.color;
                ctx.globalAlpha = this.life / 30;
                ctx.fillRect(this.x, this.y, this.size, this.size);
                ctx.globalAlpha = 1;
            }
        }

        function createExplosion(x, y, color) {
            for (let i = 0; i < 12; i++) {
                particles.push(new Particle(x, y, color));
            }
        }

        // 初始化地图
        function initMap() {
            walls = [];
            for (let row = 0; row < ROWS; row++) {
                for (let col = 0; col < COLS; col++) {
                    const type = mapData[row] ? mapData[row][col] : 0;
                    walls.push({
                        x: col * CELL_SIZE,
                        y: row * CELL_SIZE,
                        width: CELL_SIZE,
                        height: CELL_SIZE,
                        type: type,
                        row: row,
                        col: col
                    });
                }
            }
        }

        // 初始化游戏
        function initGame() {
            score = 0;
            playerLives = 3;
            enemies = [];
            bullets = [];
            particles = [];
            enemySpawnTimer = 0;
            
            initMap();
            
            player = new Tank(100, 500, 'player');
            player.flashTimer = 60;
            
            spawnEnemy();
            updateScore();
        }

        function spawnEnemy() {
            if (enemies.length >= maxEnemies) return;
            
            const spawnPoints = [
                { x: 50, y: 50 },
                { x: 350, y: 50 },
                { x: 700, y: 50 }
            ];
            
            const point = spawnPoints[Math.floor(Math.random() * spawnPoints.length)];
            const enemy = new Tank(point.x, point.y, 'enemy', DOWN);
            enemy.flashTimer = 30;
            enemies.push(enemy);
        }

        function updateScore() {
            const hearts = '❤'.repeat(Math.max(0, playerLives));
            document.getElementById('score').innerHTML = `得分: ${score} | 生命: ${hearts}`;
        }

        function gameOver() {
            gameRunning = false;
            document.getElementById('finalScore').textContent = `最终得分: ${score}`;
            document.getElementById('gameOver').style.display = 'block';
        }

        // 游戏主循环
        function gameLoop() {
            if (!gameRunning) return;

            // 更新
            player.update();
            
            for (let enemy of enemies) {
                enemy.update();
            }
            
            for (let bullet of bullets) {
                bullet.update();
            }
            
            for (let particle of particles) {
                particle.update();
            }

            // 清理
            bullets = bullets.filter(b => b.alive);
            particles = particles.filter(p => p.life > 0);
            enemies = enemies.filter(e => e.alive);

            // 生成敌人
            enemySpawnTimer++;
            if (enemySpawnTimer >= enemySpawnInterval) {
                spawnEnemy();
                enemySpawnTimer = 0;
            }

            // 绘制
            ctx.fillStyle = '#000';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // 绘制网格背景（微弱）
            ctx.strokeStyle = '#111';
            ctx.lineWidth = 1;
            for (let i = 0; i <= COLS; i++) {
                ctx.beginPath();
                ctx.moveTo(i * CELL_SIZE, 0);
                ctx.lineTo(i * CELL_SIZE, canvas.height);
                ctx.stroke();
            }
            for (let i = 0; i <= ROWS; i++) {
                ctx.beginPath();
                ctx.moveTo(0, i * CELL_SIZE);
                ctx.lineTo(canvas.width, i * CELL_SIZE);
                ctx.stroke();
            }

            // 绘制墙壁
            for (let wall of walls) {
                if (wall.type === 0) continue;
                
                if (wall.type === 1) { // 砖墙
                    ctx.fillStyle = '#8B4513';
                    ctx.fillRect(wall.x, wall.y, wall.width, wall.height);
                    ctx.fillStyle = '#A0522D';
                    ctx.fillRect(wall.x + 2, wall.y + 2, wall.width - 4, wall.height - 4);
                    ctx.strokeStyle = '#654321';
                    ctx.lineWidth = 1;
                    ctx.strokeRect(wall.x, wall.y, wall.width, wall.height);
                } else if (wall.type === 2) { // 钢墙
                    ctx.fillStyle = '#888';
                    ctx.fillRect(wall.x, wall.y, wall.width, wall.height);
                    ctx.fillStyle = '#aaa';
                    ctx.fillRect(wall.x + 2, wall.y + 2, wall.width - 4, wall.height - 4);
                    ctx.strokeStyle = '#666';
                    ctx.lineWidth = 1;
                    ctx.strokeRect(wall.x, wall.y, wall.width, wall.height);
                } else if (wall.type === 3) { // 基地
                    ctx.fillStyle = '#ffcc00';
                    ctx.fillRect(wall.x, wall.y, wall.width, wall.height);
                    ctx.fillStyle = '#ffff00';
                    ctx.fillRect(wall.x + 4, wall.y + 4, wall.width - 8, wall.height - 8);
                    ctx.strokeStyle = '#cc9900';
                    ctx.lineWidth = 2;
                    ctx.strokeRect(wall.x, wall.y, wall.width, wall.height);
                    // 基地标志
                    ctx.fillStyle = '#cc0000';
                    ctx.font = 'bold 14px Arial';
                    ctx.textAlign = 'center';
                    ctx.fillText('★', wall.x + wall.width/2, wall.y + wall.height/2 + 5);
                }
            }

            // 绘制游戏对象
            for (let bullet of bullets) {
                bullet.draw();
            }
            
            for (let particle of particles) {
                particle.draw();
            }
            
            for (let enemy of enemies) {
                enemy.draw();
            }
            
            if (player.alive) {
                player.draw();
            }

            requestAnimationFrame(gameLoop);
        }

        // 开始游戏
        document.getElementById('startBtn').addEventListener('click', () => {
            document.getElementById('startScreen').style.display = 'none';
            gameRunning = true;
            initGame();
            gameLoop();
        });

        // 重新开始
        document.getElementById('restartBtn').addEventListener('click', () => {
            document.getElementById('gameOver').style.display = 'none';
            gameRunning = true;
            initGame();
            gameLoop();
        });
    </script>
</body>
</html>
'''


def generate_game(output_path="tank_battle.html"):
    """生成坦克大战 HTML 游戏文件"""
    # 确保路径是绝对路径或相对于当前脚本
    if not os.path.isabs(output_path):
        output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_path)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(HTML_CONTENT)
    
    print(f"✅ 坦克大战游戏已生成: {output_path}")
    return output_path


def open_game(html_path):
    """用浏览器打开游戏"""
    print(f"🎮 正在启动游戏...")
    webbrowser.open(f'file://{os.path.abspath(html_path)}')


if __name__ == '__main__':
    html_file = generate_game()
    open_game(html_file)
