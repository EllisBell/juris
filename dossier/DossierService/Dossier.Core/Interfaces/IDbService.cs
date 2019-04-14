using System.Collections.Generic;
using Dossier.Core.Entities;

namespace Dossier.Core.Interfaces {
    public interface IDbService {
        IEnumerable<Folder> GetFolders();

        Folder GetFolder(int id);

        IEnumerable<SavedAcordao> GetSavedAcordaos();

        SavedAcordao GetSavedAcordao(int id);
    }
}