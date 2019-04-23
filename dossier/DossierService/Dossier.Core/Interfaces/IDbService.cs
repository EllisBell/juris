using System.Collections.Generic;
using System.Threading.Tasks;
using Dossier.Core.Entities;

namespace Dossier.Core.Interfaces {
    public interface IDbService {
        Task<IEnumerable<Folder>> GetFolders();

        Task<Folder> GetFolder(int id);

        Task CreateFolder(Folder newFolder);

        Task UpdateFolder(Folder updatedFolder);

        Task DeleteFolder(int id);

        Task<IEnumerable<SavedAcordao>> GetSavedAcordaos();

        Task<SavedAcordao> GetSavedAcordao(int id);

        Task UpdateSavedAcordao(SavedAcordao updatedAcordao);

        Task DeleteSavedAcordao(int id);

        Task AddAcordaoToFolder(int folderId, SavedAcordao acordao);

        Task AddCommentToAcordao(int acordaoId, Comment comment); 
        Task<Comment> GetComment(int id);
    }
}