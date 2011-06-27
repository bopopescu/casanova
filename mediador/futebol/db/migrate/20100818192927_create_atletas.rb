class CreateAtletas < ActiveRecord::Migration
  def self.up
    create_table :atletas do |t|
      t.string :apelido
      t.string :nome
      t.date :nascimento

      t.timestamps
    end
  end

  def self.down
    drop_table :atletas
  end
end
