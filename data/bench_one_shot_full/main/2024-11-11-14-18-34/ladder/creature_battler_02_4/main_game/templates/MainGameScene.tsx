import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { PlayerCard } from "@/components/ui/custom/player/player_card";

interface Skill {
  __type: "Skill"
  uid: string
  display_name: string
  description: string
  stats: {
    base_damage: number
  }
  meta: {
    prototype_id: string
    category: string
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
    category: string
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
  meta: {
    prototype_id: string
    category: string
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
  stats: Record<string, unknown>
  meta: Record<string, unknown>
  collections: Record<string, unknown>
  uid: string
  display_name: string
  description: string
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data.entities.player_creature
  const botCreature = props.data.entities.bot_creature
  const player = props.data.entities.player
  const bot = props.data.entities.bot

  if (!playerCreature || !botCreature || !player || !bot) {
    return <div className="h-screen w-screen flex items-center justify-center">
      Loading battle...
    </div>
  }

  const availableSkills = playerCreature.collections.skills.filter(skill => 
    availableButtonSlugs.includes(skill.meta.prototype_id)
  )

  return (
    <div className="h-screen w-screen flex flex-col">
      {/* HUD */}
      <div className="h-[12.5%] min-h-[60px] bg-slate-800 p-4 flex justify-between items-center">
        <PlayerCard 
          uid={player.uid}
          name={player.display_name}
          imageUrl={`/api/images/players/${player.meta.prototype_id}`}
        />
        <PlayerCard 
          uid={bot.uid}
          name={bot.display_name}
          imageUrl={`/api/images/players/${bot.meta.prototype_id}`}
        />
      </div>

      {/* Battlefield */}
      <div className="h-[50%] min-h-[200px] bg-slate-700 flex justify-between items-center px-16">
        <div className="transform translate-y-8">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            currentHp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
            imageUrl={`/api/images/creatures/${playerCreature.meta.prototype_id}`}
          />
        </div>
        
        <div className="transform -translate-y-8">
          <CreatureCard
            uid={botCreature.uid}
            name={botCreature.display_name}
            currentHp={botCreature.stats.hp}
            maxHp={botCreature.stats.max_hp}
            imageUrl={`/api/images/creatures/${botCreature.meta.prototype_id}`}
          />
        </div>
      </div>

      {/* Controls */}
      <div className="h-[37.5%] min-h-[150px] bg-slate-800 p-4">
        <div className="grid grid-cols-2 gap-4 h-full">
          {availableSkills.length > 0 ? (
            availableSkills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                name={skill.display_name}
                description={skill.description}
                stats={{
                  damage: skill.stats.base_damage
                }}
                onClick={() => emitButtonClick(skill.meta.prototype_id)}
              />
            ))
          ) : (
            <div className="col-span-2 flex items-center justify-center text-slate-400">
              No skills available
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
