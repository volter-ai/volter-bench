import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { PlayerCard } from "@/components/ui/custom/player/player_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"

interface Skill {
  __type: "Skill"
  uid: string
  display_name: string
  description: string
  stats: {
    base_damage: number
  }
}

interface Creature {
  __type: "Creature"
  uid: string
  display_name: string
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
}

interface GameUIData {
  entities: {
    player: Player
    opponent: Player
    player_creature: Creature
    opponent_creature: Creature
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const { player_creature, opponent_creature, player, opponent } = props.data.entities

  const getSkillBySlug = (slug: string) => {
    return player_creature?.collections.skills.find(
      skill => skill.uid === slug || skill.display_name.toLowerCase() === slug
    )
  }

  return (
    <div className="w-full h-full grid grid-rows-[auto_1fr_auto] bg-background">
      {/* HUD */}
      {player && opponent && (
        <nav className="p-4 border-b flex justify-between items-center">
          <div className="flex items-center gap-2">
            <Shield className="h-5 w-5" />
            <span>{player.display_name}</span>
          </div>
          <div className="flex items-center gap-2">
            <Swords className="h-5 w-5" />
            <span>{opponent.display_name}</span>
          </div>
        </nav>
      )}

      {/* Battlefield */}
      <div className="flex justify-between items-center p-8 gap-8">
        <div className="flex flex-col items-center gap-4">
          {player && (
            <PlayerCard
              uid={player.uid}
              name={player.display_name}
              imageUrl="/placeholder-player.png"
            />
          )}
          {player_creature && (
            <CreatureCard
              uid={player_creature.uid}
              name={player_creature.display_name}
              currentHp={player_creature.stats.hp}
              maxHp={player_creature.stats.max_hp}
              imageUrl="/placeholder-creature.png"
            />
          )}
        </div>

        <div className="flex flex-col items-center gap-4">
          {opponent && (
            <PlayerCard
              uid={opponent.uid}
              name={opponent.display_name}
              imageUrl="/placeholder-opponent.png"
            />
          )}
          {opponent_creature && (
            <CreatureCard
              uid={opponent_creature.uid}
              name={opponent_creature.display_name}
              currentHp={opponent_creature.stats.hp}
              maxHp={opponent_creature.stats.max_hp}
              imageUrl="/placeholder-creature.png"
            />
          )}
        </div>
      </div>

      {/* Skills UI */}
      <div className="p-4 border-t">
        <div className="grid grid-cols-2 gap-4 max-w-md mx-auto">
          {availableButtonSlugs.map((slug) => {
            const skill = getSkillBySlug(slug)
            if (!skill) return null
            
            return (
              <SkillButton
                key={slug}
                uid={skill.uid}
                name={skill.display_name}
                description={skill.description}
                damage={skill.stats.base_damage}
                onClick={() => emitButtonClick(slug)}
              />
            )
          })}
        </div>
      </div>
    </div>
  )
}
