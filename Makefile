##
## EPITECH PROJECT, 2018
## Gomoku
## File description:
## Makefile
##

SRCS		=	src/Main.cpp \

OBJS		= 	$(SRCS:.cpp=.o)

# Compile Flags, Include Paths and Library Paths
CXXFLAGS	= 	-Wall -Wextra -Werror -W -std=c++17 -Ofast
CPPFLAGS 	=	-I ./inc

NAME 		=	gomoku

# ==========================================================================

all:		$(NAME)

$(NAME):	$(OBJS)
		$(CXX) -o $(NAME) $(OBJS) $(LDFLAGS)

clean:
		$(RM) $(OBJS)

fclean: 	clean
		$(RM) $(NAME)

re:		fclean all

.PHONY:		all clean fclean re debug run tests
