# encoding: utf-8

import pytest

from web.contentment.taxonomy import Taxonomy


@pytest.fixture(scope='module')
def connection(request):
	from mongoengine import connect
	from .fixture import apply

	connection = connect('testing')
	apply()

	request.addfinalizer(lambda: connection.drop_database('testing'))

	return connection


@pytest.fixture
def root(connection):
	from web.component.asset.model import Asset
	return Asset.objects.get(path='/careers.illicohodes.com')


class TModel(Taxonomy):
	pass


@pytest.mark.usefixtures('connection')
class TestTaxonomy:
	def test_siblings(self, root):
		assert root.children[1].siblings.count() == 5

	def test_next(self, root):
		subroot = root.children[0].children[1]
		nexts = list(root.children[0].children[2:4])
		assert subroot.nextAll.count() == 2
		assert list(subroot.nextAll) == nexts
		c = subroot
		count = 0
		while True:
			c = c.next
			if c is None:
				break
			count += 1
		assert count == 2

	def test_prev(self, root):
		subroot = root.children[0].children[2]
		prevs = list(root.children[0].children[0:2])
		assert subroot.prevAll.count() == 2
		assert list(subroot.prevAll) == prevs
		c = subroot
		count = 0
		while True:
			c = c.prev
			if c is None:
				break
			count += 1
		assert count == 2

	def test_insert_detach(self):
		parent = TModel.objects.create(name='par', path='/')
		child1 = TModel.objects.create(name='ch1', path='/1')
		child2 = TModel.objects.create(name='ch1', path='/2')

		assert parent.children.count() == 0
		assert child1.parents == []

		parent.insert(0, child1)
		parent.insert(1, child2)
		assert list(parent.children) == [child1, child2]

		child2.detach(False)
		assert list(parent.children) == [child1]

		parent.insert(0, child2)
		assert list(parent.children) == [child2, child1]
