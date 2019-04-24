using System.Collections.Generic;
using Dossier.Core.Entities;
using Dossier.Core.Interfaces;
using Dossier.Core.Exceptions;
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
            var folderToUpdate = await GetFolder(updatedFolder.Id);
            if(folderToUpdate != null) {
                _context.Entry(folderToUpdate).CurrentValues.SetValues(updatedFolder);
                await _context.SaveChangesAsync();
            }
            else {
                await CreateFolder(updatedFolder);
            }
        }

        public async Task DeleteFolder(int id) {
            var folderToDelete = await GetFolder(id);
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
            var folder = await GetFolder(folderId);
            acordao.Folder = folder;
            _context.SavedAcordaos.Add(acordao);
            await _context.SaveChangesAsync();
        }

        public async Task DeleteSavedAcordao(int id) {
            var acordaoToDelete = await GetSavedAcordao(id);
            if(acordaoToDelete != null) {
                _context.SavedAcordaos.Remove(acordaoToDelete);
                await _context.SaveChangesAsync();
            }
            // TODO else what? - what to do if does not exist?
        }

        public async Task UpdateSavedAcordao(SavedAcordao updatedAcordao) {
            var acordaoToUpdate = await GetSavedAcordao(updatedAcordao.Id);
            if (acordaoToUpdate == null)
            {
                await AddAcordaoToFolder(updatedAcordao.Folder.Id, updatedAcordao);
            }
            else
            {
                _context.Entry(acordaoToUpdate).CurrentValues.SetValues(updatedAcordao);
                acordaoToUpdate.Folder = updatedAcordao.Folder;
                await _context.SaveChangesAsync();
            }
        }

        public async Task AddCommentToAcordao(int acordaoId, Comment comment) {
            var acordao = await GetSavedAcordao(acordaoId);
            comment.Acordao = acordao;
            _context.Comments.Add(comment);
            await _context.SaveChangesAsync();
        }

        public async Task<Comment> GetComment(int id) => 
            await _context.Comments.SingleOrDefaultAsync(x => x.Id == id);

        public async Task UpdateCommentText(int commentId, string newText) {
            var commentToUpdate = await GetComment(commentId);
            if(commentToUpdate == null) {
                throw new NotFoundException();
            }
            else {
                commentToUpdate.Text = newText;
                await _context.SaveChangesAsync();
            }
        }

        public async Task DeleteComment(int id) {
            var commentToDelete = await GetComment(id);
            if(commentToDelete != null) {
                _context.Comments.Remove(commentToDelete);
                await _context.SaveChangesAsync();
            }
            else {
                throw new NotFoundException();
            }
        }

    }
}