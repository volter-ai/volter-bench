import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { PlayerCard } from "@/components/ui/custom/player/player_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"

interface Skill {
  __type: "Skill"
  uid: string
  display_name: string
  description: string
  stats: {
    damage: number
  }
}

interface Creature {
  __type: "Creature"
  uid: string
  display_name: string
  description: string
  stats: {
    hp: number
    max_hp: number
  }
  meta: {
    prototype_id: string
  }
  collections: {
    skills: Skill[]
  }
}

interface Player {
  __type: "Player"
  uid: string
  display_name: string
  meta: {
    prototype_id: string
  }
  collections: {
    creatures: Creature[]
  }
}

interface GameUIData {
  entities: {
    player: Player
    foe: Player
    player_creature: Creature
    foe_creature: Creature
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const { player, foe, player_creature, foe_creature } = props.data.entities

  if (!player || !foe || !player_creature || !foe_creature) {
    return <div className="h-screen w-full flex items-center justify-center">
      Loading game state...
    </div>
  }

  const handleSkillClick = (skillUid: string) => {
    if (availableButtonSlugs.includes(skillUid)) {
      emitButtonClick(skillUid)
    }
  }

  return (
    <div className="h-screen w-full flex flex-col">
      <nav className="h-16 bg-slate-800 flex items-center justify-between px-4">
        <PlayerCard
          uid={player.uid}
          name={player.display_name}
          imageUrl={`/players/${player.meta?.prototype_id || 'default'}.png`}
        />
        <PlayerCard
          uid={foe.uid}
          name={foe.display_name}
          imageUrl={`/players/${foe.meta?.prototype_id || 'default'}.png`}
        />
      </nav>

      <main className="flex-1 flex justify-between items-center px-8 bg-slate-900">
        <div className="relative">
          <span className="absolute -top-8 left-1/2 -translate-x-1/2 text-green-400">
            Your Creature
          </span>
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            hp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
            imageUrl={`/creatures/${player_creature.meta?.prototype_id || 'default'}.png`}
          />
        </div>

        <div className="relative">
          <span className="absolute -top-8 left-1/2 -translate-x-1/2 text-red-400">
            Enemy Creature
          </span>
          <CreatureCard
            uid={foe_creature.uid}
            name={foe_creature.display_name}
            hp={foe_creature.stats.hp}
            maxHp={foe_creature.stats.max_hp}
            imageUrl={`/creatures/${foe_creature.meta?.prototype_id || 'default'}.png`}
          />
        </div>
      </main>

      <section className="min-h-[200px] bg-slate-700 p-4">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {player_creature.collections.skills?.map(skill => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              name={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.damage}`}
              disabled={!availableButtonSlugs.includes(skill.uid)}
              onClick={() => handleSkillClick(skill.uid)}
            />
          ))}
        </div>
      </section>
    </div>
  )
}
