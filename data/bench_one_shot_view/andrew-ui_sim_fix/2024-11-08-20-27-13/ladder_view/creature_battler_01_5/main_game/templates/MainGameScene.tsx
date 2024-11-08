import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Sword } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"
import { PlayerCard } from "@/components/ui/custom/player/player_card"

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
  collections: {
    skills: Skill[]
  }
}

interface Player {
  __type: "Player"
  uid: string
  display_name: string
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

  return (
    <div className="h-screen w-full flex flex-col">
      {/* HUD */}
      <nav className="h-16 bg-secondary flex items-center justify-between px-4">
        {player && (
          <div className="flex items-center gap-2">
            <Shield className="w-6 h-6" />
            <PlayerCard
              uid={player.uid}
              name={player.display_name}
              imageUrl={`/players/${player.display_name.toLowerCase()}.png`}
              className="w-[200px]"
            />
          </div>
        )}
        {foe && (
          <div className="flex items-center gap-2">
            <Sword className="w-6 h-6" />
            <PlayerCard
              uid={foe.uid}
              name={foe.display_name}
              imageUrl={`/players/${foe.display_name.toLowerCase()}.png`}
              className="w-[200px]"
            />
          </div>
        )}
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex items-center justify-between px-16 bg-background">
        {player_creature && (
          <div className="flex flex-col items-center gap-2">
            <span className="text-primary font-bold">Your Creature</span>
            <CreatureCard
              uid={player_creature.uid}
              name={player_creature.display_name}
              hp={player_creature.stats.hp}
              maxHp={player_creature.stats.max_hp}
              imageUrl={`/creatures/${player_creature.display_name.toLowerCase()}.png`}
            />
          </div>
        )}

        {foe_creature && (
          <div className="flex flex-col items-center gap-2">
            <span className="text-destructive font-bold">Opponent's Creature</span>
            <CreatureCard
              uid={foe_creature.uid}
              name={foe_creature.display_name}
              hp={foe_creature.stats.hp}
              maxHp={foe_creature.stats.max_hp}
              imageUrl={`/creatures/${foe_creature.display_name.toLowerCase()}.png`}
            />
          </div>
        )}
      </div>

      {/* UI Area */}
      <div className="h-1/3 bg-secondary p-4">
        <div className="grid grid-cols-3 gap-4">
          {player_creature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              name={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.damage}`}
              disabled={!availableButtonSlugs.includes(skill.uid)}
            />
          ))}
        </div>
      </div>
    </div>
  )
}
