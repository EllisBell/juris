using System.Collections.Generic;
using Dossier.Core.Entities;
using Dossier.Core.Interfaces;
using Microsoft.EntityFrameworkCore;
using System.Linq;

namespace Dossier.Infrastructure.Data {
    public class DbService : IDbService
    {
        private readonly DossierContext _context;
        public DbService(DossierContext context) {
            _context = context;
        }

        public Folder GetFolder(int id)
        {
            return _context.Folders.SingleOrDefault(x => x.Id == id);
        }

        public IEnumerable<Folder> GetFolders()
        {
            var res = _context.Folders.Include(x => x.SavedAcordaos).ToList();
            return res;
        }


        public IEnumerable<SavedAcordao> GetSavedAcordaos()
        { 
            return _context.SavedAcordaos; 
        }

        public SavedAcordao GetSavedAcordao(int id)
        {
            return _context.SavedAcordaos.Include(x => x.Comments).SingleOrDefault(x => x.Id == id);
        }
    }
}