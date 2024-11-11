import { useCurrentButtons } from "@/lib/useChoices.ts";
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
  description: string
  stats: {
    hp: number
    max_hp: number
    attack: number
    defense: number
    speed: number
  }
  collections: {
    skills: Skill[]
  }
}

interface Player {
  __type: "Player"
  uid: string
  display_name: string
  description: string
  collections: {
    creatures: Creature[]
  }
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

  const { player, opponent, player_creature, opponent_creature } = props.data.entities

  return (
    <div className="h-screen w-screen flex flex-col bg-background">
      {/* HUD */}
      <div className="w-full p-4 bg-secondary/10 flex justify-between items-center">
        {player && (
          <PlayerCard 
            uid={player.uid}
            name={player.display_name}
            imageUrl="" // Removed hardcoded image
          />
        )}
        {opponent && (
          <PlayerCard
            uid={opponent.uid}
            name={opponent.display_name}
            imageUrl="" // Removed hardcoded image
          />
        )}
      </div>

      {/* Battlefield */}
      <div className="flex-1 flex justify-between items-center px-16 py-8">
        {player_creature && (
          <div className="relative">
            <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-primary text-primary-foreground px-3 py-1 rounded-full">
              Player
            </div>
            <CreatureCard
              uid={player_creature.uid}
              name={player_creature.display_name}
              currentHp={player_creature.stats.hp}
              maxHp={player_creature.stats.max_hp}
              imageUrl="" // Removed hardcoded image
            />
          </div>
        )}

        {opponent_creature && (
          <div className="relative">
            <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-destructive text-destructive-foreground px-3 py-1 rounded-full">
              Opponent
            </div>
            <CreatureCard
              uid={opponent_creature.uid}
              name={opponent_creature.display_name}
              currentHp={opponent_creature.stats.hp}
              maxHp={opponent_creature.stats.max_hp}
              imageUrl="" // Removed hardcoded image
            />
          </div>
        )}
      </div>

      {/* Action UI */}
      <div className="h-1/4 bg-secondary/20 p-4 overflow-y-auto">
        {player_creature?.collections.skills && player_creature.collections.skills.length > 0 ? (
          <div className="grid grid-cols-2 gap-4 max-w-2xl mx-auto">
            {player_creature.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                name={skill.display_name}
                description={skill.description}
                stats={{
                  damage: skill.stats.base_damage
                }}
              />
            ))}
          </div>
        ) : (
          <div className="text-center text-muted-foreground">
            No skills available
          </div>
        )}
      </div>
    </div>
  )
}
