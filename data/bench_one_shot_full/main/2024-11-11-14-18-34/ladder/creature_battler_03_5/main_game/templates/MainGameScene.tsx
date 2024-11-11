import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap, User, Bot } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"
import { PlayerCard } from "@/components/ui/custom/player/player_card"
import { Card } from "@/components/ui/card"

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
    <div className="h-screen w-screen aspect-video bg-background flex flex-col">
      {/* Top HUD */}
      <div className="bg-primary/10 p-4 flex justify-between items-center">
        {player && (
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl="/avatars/player.png"
            className="w-[200px] h-[80px]"
          />
        )}
        {opponent && (
          <PlayerCard
            uid={opponent.uid}
            name={opponent.display_name}
            imageUrl="/avatars/opponent.png"
            className="w-[200px] h-[80px]"
          />
        )}
      </div>

      {/* Battlefield */}
      <div className="flex-1 flex items-center justify-center px-8">
        <div className="grid grid-cols-2 gap-8 w-full">
          <div className="flex flex-col items-center gap-4">
            <div className="flex items-center gap-2">
              <User className="h-6 w-6 text-blue-500" />
              <span className="font-bold">Your Creature</span>
            </div>
            {player_creature && (
              <CreatureCard
                uid={player_creature.uid}
                name={player_creature.display_name}
                currentHp={player_creature.stats.hp}
                maxHp={player_creature.stats.max_hp}
                imageUrl={`/creatures/${player_creature.meta.prototype_id}.png`}
              />
            )}
          </div>
          <div className="flex flex-col items-center gap-4">
            <div className="flex items-center gap-2">
              <Bot className="h-6 w-6 text-red-500" />
              <span className="font-bold">Opponent's Creature</span>
            </div>
            {opponent_creature && (
              <CreatureCard
                uid={opponent_creature.uid}
                name={opponent_creature.display_name}
                currentHp={opponent_creature.stats.hp}
                maxHp={opponent_creature.stats.max_hp}
                imageUrl={`/creatures/${opponent_creature.meta.prototype_id}.png`}
              />
            )}
          </div>
        </div>
      </div>

      {/* Controls Area */}
      <Card className="mt-auto rounded-t-lg p-4">
        <div className="mb-4">
          <h3 className="text-lg font-bold mb-2">Battle Log</h3>
          <div className="bg-muted p-2 rounded-md h-[80px] overflow-y-auto">
            {/* Battle text would be inserted here */}
            <p className="text-sm">What will you do?</p>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          {player_creature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              name={skill.display_name}
              description={skill.description}
              damage={skill.stats.base_damage}
            />
          ))}
        </div>
      </Card>
    </div>
  )
}
