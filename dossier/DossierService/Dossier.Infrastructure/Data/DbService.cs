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
           await _context.Folders
                .Include(x => x.SavedAcordaos)
                .ThenInclude(a => a.Comments)
                .SingleOrDefaultAsync(x => x.Id == id);

        public async Task<IEnumerable<Folder>> GetFolders() =>
            // https://docs.microsoft.com/en-us/ef/core/querying/async
            await _context.Folders.Include(x => x.SavedAcordaos).ToListAsync();

        
        public async Task CreateFolder(Folder newFolder) {
            _context.Folders.Add(newFolder);
            await _context.SaveChangesAsync();
        }

        public async Task UpdateFolder(Folder updatedFolder) {
            var folderToUpdate = await _context.Folders.SingleOrDefaultAsync(x => x.Id == updatedFolder.Id);
            if(folderToUpdate != null) {
                _context.Entry(folderToUpdate).CurrentValues.SetValues(updatedFolder);
                await _context.SaveChangesAsync();
            }
            else {
                await CreateFolder(updatedFolder);
            }
        }

        public async Task DeleteFolder(int id) {
            var folderToDelete = await _context.Folders.SingleOrDefaultAsync(x => x.Id == id);
            if(folderToDelete != null) {
                _context.Folders.Remove(folderToDelete);
                await _context.SaveChangesAsync();
            }   
        }

        public async Task<IEnumerable<SavedAcordao>> GetSavedAcordaos() => 
            await _context.SavedAcordaos.Include(x => x.Comments).ToListAsync();

        public async Task<SavedAcordao> GetSavedAcordao(int id) => 
            await _context.SavedAcordaos.Include(x => x.Comments).SingleOrDefaultAsync(x => x.Id == id);

        public async Task AddAcordaoToFolder(int folderId, SavedAcordao acordao) {
            var folder = await _context.Folders.SingleOrDefaultAsync(x => x.Id == folderId);
            acordao.Folder = folder;
            _context.SavedAcordaos.Add(acordao);
            await _context.SaveChangesAsync();
        }

        public async Task DeleteSavedAcordao(int id) {
            var acordaoToDelete = await _context.SavedAcordaos.SingleOrDefaultAsync(x => x.Id == id);
            if(acordaoToDelete != null) {
                _context.SavedAcordaos.Remove(acordaoToDelete);
                await _context.SaveChangesAsync();
            }
        }

        public async Task UpdateSavedAcordao(SavedAcordao updatedAcordao) {
            var acordaoToUpdate = await _context.SavedAcordaos.SingleOrDefaultAsync(x => x.Id == updatedAcordao.Id);
            if(acordaoToUpdate != null) {
                _context.Entry(acordaoToUpdate).CurrentValues.SetValues(updatedAcordao);
                acordaoToUpdate.Folder = updatedAcordao.Folder;
                await _context.SaveChangesAsync();
            }
            else {
                await AddAcordaoToFolder(updatedAcordao.Folder.Id, updatedAcordao);
            }
        }

        public async Task AddCommentToAcordao(int acordaoId, Comment comment) {
            var acordao = await _context.SavedAcordaos.SingleOrDefaultAsync(x => x.Id == acordaoId);
            comment.Acordao = acordao;
            _context.Comments.Add(comment);
            await _context.SaveChangesAsync();
        }

        public async Task<Comment> GetComment(int id) => 
            await _context.Comments.SingleOrDefaultAsync(x => x.Id == id);
    }
}