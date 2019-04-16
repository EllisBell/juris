using System.Collections.Generic;
using Dossier.Core.Entities;
using Dossier.Core.Interfaces;
using Microsoft.EntityFrameworkCore;
using System.Linq;
using System.Threading.Tasks;

namespace Dossier.Infrastructure.Data {
    public class DbService : IDbService
    {
        private readonly DossierContext _context;
        public DbService(DossierContext context) {
            _context = context;
        }

        public async Task<Folder> GetFolder(int id) => 
           await _context.Folders.Include(x => x.SavedAcordaos).SingleOrDefaultAsync(x => x.Id == id);

        public async Task<IEnumerable<Folder>> GetFolders() =>
            // https://docs.microsoft.com/en-us/ef/core/querying/async
            await _context.Folders.Include(x => x.SavedAcordaos).ToListAsync();

        public void CreateFolder(Folder newFolder) {
            _context.Folders.Add(newFolder);
            _context.SaveChanges();
        }

        public void UpdateFolder(Folder updatedFolder) {
            var folderToUpdate = _context.Folders.SingleOrDefault(x => x.Id == updatedFolder.Id);
            _context.Entry(folderToUpdate).CurrentValues.SetValues(updatedFolder);
            _context.SaveChanges();
        }


        public async Task<IEnumerable<SavedAcordao>> GetSavedAcordaos() => 
            await _context.SavedAcordaos.Include(x => x.Comments).ToListAsync();

        public async Task<SavedAcordao> GetSavedAcordao(int id) => 
            await _context.SavedAcordaos.Include(x => x.Comments).SingleOrDefaultAsync(x => x.Id == id);
    }
}