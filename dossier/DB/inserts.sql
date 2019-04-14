-- Folders

INSERT INTO public."Folders"(
	"Id", "Name")
	VALUES (1, 'test');
	
INSERT INTO public."Folders"(
	"Id", "Name")
	VALUES (2, 'My Folder 1');
	
INSERT INTO public."Folders"(
	"Id", "Name")
	VALUES (3, 'My Folder 2'); 


-- Saved Acordaos
INSERT INTO public."SavedAcordao"(
	"Id", "OriginalAcordaoId", "FolderId")
	VALUES (1, 2, 1);
	
INSERT INTO public."SavedAcordao"(
	"Id", "OriginalAcordaoId", "FolderId")
	VALUES (2, 5, 1);
	
INSERT INTO public."SavedAcordao"(
	"Id", "OriginalAcordaoId", "FolderId")
	VALUES (3, 2, 2);
	
INSERT INTO public."SavedAcordao"(
	"Id", "OriginalAcordaoId", "FolderId")
	VALUES (4, 4, 3);