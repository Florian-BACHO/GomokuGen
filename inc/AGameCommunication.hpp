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

namespace Gomoku {
	class AGameCommunication;

	using Board = std::vector<std::vector<std::vector<float>>>;
};

class Gomoku::AGameCommunication {
public:
	AGameCommunication() {
		_handlers["START"] = [this](const std::vector<std::string> &params)
			{handleStart(params);};
	}

	void operator()() {
		auto line = readLine();

		handleCommand(line);
	}

	virtual bool start(uint32_t width, uint32_t height) = 0;

protected:
	Board _board;

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
		strs.push_back(txt.substr(initialPos, std::min(pos, txt.size())
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

	void handleStart(const std::vector<std::string> &) {
	        start(0, 0);
	}

private:
	std::unordered_map<std::string,
			   std::function<void(const std::vector<std::string> &)>>
	_handlers;
};
