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
  description: string
  stats: {
    hp: number
    max_hp: number
    attack: number
    defense: number
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
    <div className="grid grid-rows-[auto_1fr_auto] h-screen bg-background">
      {/* HUD */}
      <nav className="flex justify-between items-center p-4 bg-muted">
        {player && (
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl="/default-player.png"
          />
        )}
        <div className="flex items-center gap-2">
          <Swords className="h-5 w-5" />
          <span className="font-bold">VS</span>
        </div>
        {opponent && (
          <PlayerCard
            uid={opponent.uid}
            name={opponent.display_name}
            imageUrl="/default-opponent.png"
          />
        )}
      </nav>

      {/* Battlefield */}
      <main className="flex justify-between items-center p-8 gap-8">
        <div className="flex flex-col items-center gap-4">
          <span className="text-lg font-bold">Your Creature</span>
          {player_creature && (
            <CreatureCard
              uid={player_creature.uid}
              name={player_creature.display_name}
              currentHp={player_creature.stats.hp}
              maxHp={player_creature.stats.max_hp}
              imageUrl="/default-creature.png"
            />
          )}
        </div>

        <div className="flex flex-col items-center gap-4">
          <span className="text-lg font-bold">Opponent's Creature</span>
          {opponent_creature && (
            <CreatureCard
              uid={opponent_creature.uid}
              name={opponent_creature.display_name}
              currentHp={opponent_creature.stats.hp}
              maxHp={opponent_creature.stats.max_hp}
              imageUrl="/default-creature.png"
            />
          )}
        </div>
      </main>

      {/* Bottom UI */}
      <div className="p-4 bg-muted">
        <div className="flex flex-wrap gap-2 justify-center">
          {player_creature?.collections?.skills?.length > 0 ? (
            player_creature.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                name={skill.display_name}
                description={skill.description}
                damage={skill.stats.base_damage}
              />
            ))
          ) : (
            <div className="text-center text-muted-foreground">
              No skills available
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
