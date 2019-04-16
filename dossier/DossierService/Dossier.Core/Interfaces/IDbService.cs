using System.Collections.Generic;
using System.Threading.Tasks;
using Dossier.Core.Entities;

namespace Dossier.Core.Interfaces {
    public interface IDbService {
        Task<IEnumerable<Folder>> GetFolders();

        Task<Folder> GetFolder(int id);

        Task<IEnumerable<SavedAcordao>> GetSavedAcordaos();

        Task<SavedAcordao> GetSavedAcordao(int id);
    }
}