from fastapi import APIRouter
from fastapi.params import Form
from fastapi.requests import Request
from fastapi.responses import RedirectResponse

from ..models import Segment, NamedEntity, Sentence, TokenizeResponse

router = APIRouter()


@router.get('/', include_in_schema=False)
async def index() -> RedirectResponse:
    return RedirectResponse('/docs')


@router.post('/', response_model=TokenizeResponse)
async def tokenize(
    request: Request,
    sentence_list: str = Form(
        ...,
        description=r'Sentence list for CKIP tagging, split multiple sentences by linebreak(`\n`)',
        example='美國參議院針對今天總統布希所提名的勞工部長趙小蘭展開認可聽證會，預料她將會很順利通過參議院支持，成為該國有史以來第一位的華裔女性內閣成員。'
    )
) -> TokenizeResponse:
    sentence_list = sentence_list.split('\n')

    words_list = request.app.ws(sentence_list)
    part_of_speech_tags_list = request.app.pos(words_list)
    named_entities_list = request.app.ner(words_list, part_of_speech_tags_list)

    assert len(sentence_list) == len(words_list) == len(part_of_speech_tags_list) == len(named_entities_list)

    response = TokenizeResponse()

    for sentence, words, part_of_speech_tags, named_entities in zip(sentence_list, words_list, part_of_speech_tags_list, named_entities_list):
        sentence_response = Sentence()

        for word, part_of_speech_tag in zip(words, part_of_speech_tags):
            sentence_response.segments.append(Segment(
                word=word,
                pos=part_of_speech_tag
            ))

        for named_entity in sorted(named_entities):
            sentence_response.entities.append(NamedEntity(
                word=named_entity[3],
                type=named_entity[2],
                start=named_entity[0],
                end=named_entity[1]
            ))

        response.sentences.append(sentence_response)

    return response
