%{
unsigned int charCount=0, wordCount=0, lineCount=0;
%}
digit	[0-9]
%%
{digit}	{ ECHO; printf(“ is digit.\n”); }
%%
int main(int argc, char *argv[]) {
	yylex();
 	return(0);
}