import pendulum
import pytest
import uuid

from seedwork.mixin.entity_props import EntityPropsMixin


@pytest.fixture
def entity_props():
    class EntityProps(EntityPropsMixin):
        pass

    return EntityProps()


def test_create_default_fields(entity_props):
    """
    should be able to create a class with default fields already set
    """

    props = entity_props

    assert props.id is not None
    assert props.created_at is not None
    assert props.updated_at is not None


def test_id_immutability(entity_props):
    """
    should not be able to change the id field
    """

    props = entity_props

    new_id = uuid.uuid4()

    with pytest.raises(
        TypeError, match='"id" has allow_mutation set to False and cannot be assigned'
    ):
        props.id = new_id


def test_created_at_field_immutability(entity_props):
    """
    should not be able to change the created_at field
    """

    props = entity_props

    new_created_at = pendulum.now()

    with pytest.raises(
        TypeError,
        match='"created_at" has allow_mutation set to False and cannot be assigned',
    ):
        props.created_at = new_created_at


def test_timezone_field(entity_props):
    """
    should be able to have a timezone info from datetime fields
    """

    props = entity_props

    assert props.created_at.tz is not None

    assert props.updated_at.tz is not None
