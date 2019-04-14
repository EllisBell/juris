using Dossier.Core.Interfaces;
using Dossier.Core.Entities;
using System.Linq;

namespace Dossier.Core.Services
{
    public class FolderService : IFolderService
    {
      //  private IRepository<Folder> _repo;
        private IDbService _dbService;
        // public FolderService(IRepository<Folder> repo) 
        // {
        //     _repo = repo;
        // }

        public FolderService(IDbService dbService) 
        {
            _dbService = dbService;
        }

        public System.Collections.Generic.IEnumerable<Folder> GetAllFolders()
        {
            return _dbService.GetFolders();
        }

        public System.Collections.Generic.IEnumerable<Folder> GetUserFolders(int userId)
        {
            throw new System.NotImplementedException();
        }
    }
}