using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Http;
using Dossier.Api.Models;
using Dossier.Core.Interfaces;
using Dossier.Core.Entities;

namespace Dossier.Api.Controllers
{
    [ApiVersion("1.0")]
    [Route("api/v{version:apiVersion}/[controller]")]
    //[Route("api/[controller]")]
    [ApiController]
    public class FoldersController : DossierBaseController
    {
        private readonly IDbService _dbService;
        
        public FoldersController(IDbService dbService) {
            _dbService = dbService;
        }
        
        /// <summary>
        /// Gets all folders.
        /// </summary>
        // GET api/folders/5
        // GET api/folders
        [HttpGet]
        public async Task<ActionResult<IEnumerable<FolderDto>>> Get()
        {
           var result = await _dbService.GetFolders();

           return result.Select(x => FolderDto.FromEntity(x)).ToList();
        }

        /// <summary>
        /// Gets a specific folder.
        /// </summary>
        // GET api/folders/5
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        [HttpGet("{id}")]
        public async Task<ActionResult<FolderDto>> Get(int id)
        {
            var result = await _dbService.GetFolder(id);
            
            if(result is null)
                return NotFound();

            return FolderDto.FromEntity(result);
        }

        /// <summary>
        /// Creates a new folder.
        /// </summary>
        // POST api/folders
        [ProducesResponseType(StatusCodes.Status201Created)]
        [HttpPost]
        public async Task<IActionResult> CreateFolder(FolderDto folderDto) {
            Folder folderEntity = new Folder() {
                Name = folderDto.Name
            };

            await _dbService.CreateFolder(folderEntity);
            folderDto.Id = folderEntity.Id;
            // N.b. having to use API version for this to work
            return CreatedAtAction(nameof(Get), new {id = folderEntity.Id, version = ApiVersion}, 
                                    folderDto);
        }

        /// <summary>
        /// Updates a specific folder.
        /// </summary>
        // PUT api/folders/5
        [ProducesResponseType(StatusCodes.Status201Created)]
        [HttpPut("{id}")]
        public async Task<IActionResult> UpdateFolder(int id, FolderDto folderDto) {
            // TODO clean up how errors are being handled, response content etc.
            // TODO should not be passing id in this dto?
            if (id != folderDto.Id) {
                return BadRequest("The folder ID does not match the ID in the URL");
            }
            // TODO reassess how to map from DTO to entity model
            var folderEntity = new Folder() {
                Id = folderDto.Id,
                Name = folderDto.Name
            };
            await _dbService.UpdateFolder(folderEntity);
            folderDto.Id = folderEntity.Id;

            return CreatedAtAction(nameof(Get), new {id = folderEntity.Id, version = ApiVersion}, 
                                    folderDto);
        }

        /// <summary>
        /// Deletes a specific folder.
        /// </summary>
        // DELETE api/folders/5
        [ProducesResponseType(StatusCodes.Status204NoContent)]
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteFolder(int id) {
            await _dbService.DeleteFolder(id);
            return NoContent();
        }

        /// <summary>
        /// Gets the acordaos saved in a specific folder.
        /// </summary>
        // GET api/folders/5/acordaos
        [HttpGet("{id}/acordaos")]
        public async Task<ActionResult<IEnumerable<SavedAcordaoDto>>> GetFolderAcordaos(int id) {
            var folder = await _dbService.GetFolder(id);
            return folder.SavedAcordaos.Select(x => SavedAcordaoDto.FromEntity(x)).ToList();
        }

        /// <summary>
        /// Adds an acordao to a specific folder.
        /// </summary>
        // POST api/folders/5/acordaos
        [ProducesResponseType(StatusCodes.Status201Created)]
        [HttpPost("{id}/acordaos")]
        public async Task<IActionResult> AddAcordaoToFolder(int id, SavedAcordaoDto acordaoDto) {
            var acordaoEntity = new SavedAcordao() {
                OriginalAcordaoId = acordaoDto.AcordaoId,
            };

            await _dbService.AddAcordaoToFolder(id, acordaoEntity);
            acordaoDto.Id = acordaoEntity.Id;

            return CreatedAtAction("Get", "savedacordaos", new {id = acordaoDto.Id, version = ApiVersion}, 
                                    acordaoDto);
        }



    }
}
