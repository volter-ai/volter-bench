import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"
import { PlayerCard } from "@/components/ui/custom/player/player_card"

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
  meta: {
    prototype_id: string
  }
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
    bot: Player
    player_creature: Creature
    bot_creature: Creature
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const { player, bot, player_creature, bot_creature } = props.data.entities

  // Ensure we have both the creature skills and available button slugs
  const availableSkills = player_creature?.collections?.skills?.filter(skill => 
    Array.isArray(availableButtonSlugs) && 
    availableButtonSlugs.includes(skill.uid)
  ) || []

  return (
    <div className="h-screen w-screen flex flex-col bg-background">
      {/* HUD */}
      <nav className="h-[10%] min-h-[60px] flex items-center justify-between px-6 border-b">
        {player && (
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl={`/players/${player.meta?.prototype_id || 'default'}.png`}
          />
        )}
        {bot && (
          <PlayerCard
            uid={bot.uid}
            name={bot.display_name}
            imageUrl={`/players/${bot.meta?.prototype_id || 'default'}.png`}
          />
        )}
      </nav>

      {/* Battlefield */}
      <div className="h-[60%] min-h-[300px] flex justify-between items-center px-12">
        <div className="flex flex-col items-center gap-4">
          <span className="text-lg font-bold">Your Creature</span>
          {player_creature && (
            <CreatureCard
              uid={player_creature.uid}
              name={player_creature.display_name}
              currentHp={player_creature.stats.hp}
              maxHp={player_creature.stats.max_hp}
              imageUrl={`/creatures/${player_creature.meta?.prototype_id || 'default'}.png`}
            />
          )}
        </div>

        <div className="flex flex-col items-center gap-4">
          <span className="text-lg font-bold">Opponent's Creature</span>
          {bot_creature && (
            <CreatureCard
              uid={bot_creature.uid}
              name={bot_creature.display_name}
              currentHp={bot_creature.stats.hp}
              maxHp={bot_creature.stats.max_hp}
              imageUrl={`/creatures/${bot_creature.meta?.prototype_id || 'default'}.png`}
            />
          )}
        </div>
      </div>

      {/* Skills/Controls */}
      <div className="h-[30%] min-h-[200px] flex flex-col items-center justify-center p-6 border-t">
        {Array.isArray(availableSkills) && availableSkills.length > 0 ? (
          <div className="grid grid-cols-2 gap-4 w-full max-w-2xl">
            {availableSkills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={{
                  damage: skill.stats.base_damage
                }}
                onClick={() => emitButtonClick(skill.uid)}
              />
            ))}
          </div>
        ) : (
          <div className="text-center text-gray-500">
            Waiting for available actions...
          </div>
        )}
      </div>
    </div>
  )
}
