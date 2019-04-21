using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Dossier.Api.Models;
using Dossier.Core.Interfaces;
using Dossier.Core.Entities;

namespace Dossier.Api.Controllers
{
    // TODO add exception handling
    [Route("api/[controller]")]
    [ApiController]
    public class FoldersController : ControllerBase
    {
        private readonly IDbService _dbService;
        
        public FoldersController(IDbService dbService) {
            _dbService = dbService;
        }
        
        // GET api/folders
        [HttpGet]
        public async Task<ActionResult<IEnumerable<FolderDto>>> Get()
        {
           var result = await _dbService.GetFolders();

           return result.Select(x => FolderDto.FromEntity(x)).ToList();
        }

        // GET api/folders/5
        [HttpGet("{id}")]
        public async Task<ActionResult<FolderDto>> Get(int id)
        {
            var result = await _dbService.GetFolder(id);
            return FolderDto.FromEntity(result);
        }

        // POST api/folders
        [HttpPost]
        public async Task<IActionResult> CreateFolder(FolderDto folder) {
            Folder folderEntity = new Folder() {
                Name = folder.Name
            };

            await _dbService.CreateFolder(folderEntity);
            folder.Id = folderEntity.Id;

            return CreatedAtAction(nameof(Get), new {id = folderEntity.Id}, folder);
        }

        // PUT api/folders/5
        [HttpPut("{id}")]
        public async Task<IActionResult> UpdateFolder(int id, FolderDto folderDto) {
            // TODO clean up how errors are being handled, response content etc.
            if(id != folderDto.Id) {
                return BadRequest("You cannot change the folder Id");
            }
            var folderEntity = new Folder() {
                Id = folderDto.Id,
                Name = folderDto.Name
            };
            await _dbService.UpdateFolder(folderEntity);
            return NoContent();
        }

        // DELETE api/folders/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteFolder(int id) {
            await _dbService.DeleteFolder(id);
            return Ok();
        }

        // GET api/folders/5/acordaos
        [HttpGet("{id}/acordaos")]
        public async Task<ActionResult<IEnumerable<SavedAcordaoDto>>> GetFolderAcordaos(int id) {
            var folder = await _dbService.GetFolder(id);
            return folder.SavedAcordaos.Select(x => SavedAcordaoDto.FromEntity(x)).ToList();
        }

        // POST api/folders/5/acordaos
        [HttpPost("{id}/acordaos")]
        public async Task<IActionResult> AddAcordaoToFolder(int id, SavedAcordaoDto acordaoDto) {
            var acordaoEntity = new SavedAcordao() {
                OriginalAcordaoId = acordaoDto.AcordaoId,
            };
            await _dbService.AddAcordaoToFolder(id, acordaoEntity);
            acordaoDto.Id = acordaoEntity.Id;

            return CreatedAtAction("Get", "savedacordaos", new {id = acordaoDto.Id}, acordaoDto);
        }



    }
}
