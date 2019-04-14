using System.Collections.Generic;
using Dossier.Core.Entities;

namespace Dossier.Core.Services {
    public interface IFolderService
    {
        IEnumerable<Folder> GetAllFolders();
        IEnumerable<Folder> GetUserFolders(int userId);
    }
}