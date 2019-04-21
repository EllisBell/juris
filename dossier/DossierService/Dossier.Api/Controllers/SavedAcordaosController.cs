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
    [Route("api/[controller]")]
    [ApiController]
    public class SavedAcordaosController : ControllerBase
    {
        private readonly IDbService _dbService;
        
        public SavedAcordaosController(IDbService dbService) {
            _dbService = dbService;
        }
        
        // GET api/savedAcordaos
        [HttpGet]
        public async Task<ActionResult<IEnumerable<SavedAcordaoDto>>> Get()
        {
           var result = await _dbService.GetSavedAcordaos();
           return result.Select(x => SavedAcordaoDto.FromEntity(x)).ToList();
        }

        // GET api/savedAcordaos/5
        [HttpGet("{id}")]
        public async Task<ActionResult<SavedAcordaoDto>> Get(int id)
        {
            var sa = await _dbService.GetSavedAcordao(id);
            return SavedAcordaoDto.FromEntity(sa);
        }

        //GET api/savedacordaos/5/comments
        [HttpGet("{id}/comments")]
        public async Task<ActionResult<IEnumerable<CommentDto>>> GetAcordaoComments(int id) {
            var acordao = await _dbService.GetSavedAcordao(id);
            return acordao.Comments.Select(x => CommentDto.FromEntity(x)).ToList();
        }

        // POST api/savedacordaos/5/comments
        [HttpPost("{id}/comments")]
        public async Task<IActionResult> AddCommentToAcordao(int id, CommentDto commentDto) {
            var commentEntity = new Comment() {
                Author = commentDto.Author,
                Date = commentDto.Date,
                Text = commentDto.Text
            };

            await _dbService.AddCommentToAcordao(id, commentEntity);
            commentDto.Id = commentEntity.Id;
            return CreatedAtAction("Get", "comments", new {id = commentDto.Id}, commentDto);
        }

        // DELETE api/savedacordaos/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteSavedAcordao(int id) {
            await _dbService.DeleteSavedAcordao(id);
            return Ok();
        }

    }
}
