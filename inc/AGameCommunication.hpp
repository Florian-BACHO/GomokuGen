//
// EPITECH PROJECT, 2018
// Gomoku
// File description:
// Abstract Game Communication
//

#pragma once

#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>
#include <windows.h>

namespace Gomoku {
	class AGameCommunication;

	using Board = std::vector<std::vector<std::vector<float>>>;
};

class Gomoku::AGameCommunication {
public:
	AGameCommunication() {
		_handlers["START"] = [this](const std::vector<std::string> &params)
			{handleStart(params);};
		_handlers["TURN"] = [this](const std::vector<std::string> &params)
			{handleTurn(params);};
		_handlers["BOARD"] = [this](const std::vector<std::string> &params)
			{handleBoard(params);};
		_handlers["INFO"] = [this](const std::vector<std::string> &params)
			{handleInfo(params);};
		_handlers["ABOUT"] = [this](const std::vector<std::string> &params)
			{handleEnd(params);};
	}

	void operator()() {
		auto line = readLine();

		handleCommand(line);
	}

	virtual void start(uint32_t size) = 0;
	virtual void turn(uint32_t x, uint32_t y) = 0;
	virtual void resetBoard() = 0;
	virtual void board(uint32_t x, uint32_t y, uint32_t player) = 0;
	virtual void info(const std::vector<std::string> &params) = 0;
	virtual void end() = 0;
	virtual void about() = 0;

private:
	inline std::string readLine() const noexcept {
		std::string out;

		std::getline(std::cin, out);
		return out;
	}

	size_t split(const std::string &txt, std::vector<std::string> &strs,
		     char ch) const noexcept {
		auto pos = txt.find(ch);
		size_t initialPos = 0;

		strs.clear();
		while(pos != std::string::npos) {
			strs.push_back(txt.substr(initialPos, pos - initialPos));
			initialPos = pos + 1;

			pos = txt.find( ch, initialPos );
		}
		strs.push_back(txt.substr(initialPos, min(pos, txt.size())
					  - initialPos + 1 ));

		return strs.size();
	}

	void handleCommand(const std::string &command) {
		std::vector<std::string> parsed;
		std::string cmd;

		split(command, parsed, ' ');
		if (parsed.size() == 0 ||
		    _handlers.find(parsed[0]) == _handlers.end())
			return;
		cmd = parsed[0];
		parsed.erase(parsed.begin());
		_handlers[cmd](parsed);
	}

	void handleStart(const std::vector<std::string> &vec) {
		start(std::atoi(vec[0].c_str()));
	}

	void handleTurn(const std::vector<std::string> &vec) {
		std::vector<std::string> parsed;

		split(vec[0], parsed, ',');
		turn(std::atoi(parsed[0].c_str()), std::atoi(parsed[0].c_str()));
	}

	void handleBoard(const std::vector<std::string> &vec) {
		std::string line = readLine();
		std::vector<std::string> parsed;
		uint32_t x;
		uint32_t y;
		uint32_t player;

		resetBoard();
		while (line != "DONE") {
			split(line, parsed, ',');
			x = std::atoi(parsed[0].c_str());
			y = std::atoi(parsed[1].c_str());
			player = std::atoi(parsed[2].c_str());
			board(x, y, player);
		}
	}

	void handleInfo(const std::vector<std::string> &vec) {
		info(vec);
	}

	void handleEnd(const std::vector<std::string> &) {
		end();
	}

	void handleAbout(const std::vector<std::string> &) {
		about();
	}

private:
	std::unordered_map<std::string,
			   std::function<void(const std::vector<std::string> &)>>
	_handlers;
};
