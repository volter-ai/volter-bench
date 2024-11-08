import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, SwapHorizontal } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"
import { Button } from "@/components/ui/button"

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
    skill_type: string
    is_physical: boolean
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
    sp_attack: number
    sp_defense: number
    speed: number
  }
  meta: {
    prototype_id: string
    category: string
    creature_type: string
  }
  collections: {
    skills: Skill[]
  }
}

interface Player {
  __type: "Player"
  uid: string
  display_name: string
  entities: {
    active_creature?: Creature
  }
}

interface GameUIData {
  entities: {
    player: Player
    bot: Player
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data.entities.player.entities.active_creature
  const botCreature = props.data.entities.bot.entities.active_creature

  return (
    <div className="w-full h-full aspect-w-16 aspect-h-9 bg-slate-100">
      {/* Battlefield Area */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Top Left - Bot Status */}
        <div className="flex justify-start items-start">
          {botCreature && (
            <CreatureCard
              uid={botCreature.uid}
              name={botCreature.display_name}
              image={`/creatures/${botCreature.meta.prototype_id}_front.png`}
              currentHp={botCreature.stats.hp}
              maxHp={botCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Top Right - Bot Creature */}
        <div className="flex justify-end items-start">
          <div className="relative w-48 h-48">
            {botCreature && (
              <img 
                src={`/creatures/${botCreature.meta.prototype_id}_front.png`}
                alt={botCreature.display_name}
                className="w-full h-full object-contain"
              />
            )}
          </div>
        </div>

        {/* Bottom Left - Player Creature */}
        <div className="flex justify-start items-end">
          <div className="relative w-48 h-48">
            {playerCreature && (
              <img
                src={`/creatures/${playerCreature.meta.prototype_id}_back.png`}
                alt={playerCreature.display_name}
                className="w-full h-full object-contain"
              />
            )}
          </div>
        </div>

        {/* Bottom Right - Player Status */}
        <div className="flex justify-end items-end">
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              image={`/creatures/${playerCreature.meta.prototype_id}_back.png`}
              currentHp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>
      </div>

      {/* UI Area */}
      <div className="h-1/3 p-4 bg-white">
        <div className="grid grid-cols-2 gap-4">
          {availableButtonSlugs.includes('attack') && playerCreature?.collections.skills.map(skill => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              name={skill.display_name}
              description={skill.description}
              damage={skill.stats.base_damage}
              type={skill.meta.skill_type}
            />
          ))}
          
          {availableButtonSlugs.includes('back') && (
            <Button className="flex items-center gap-2">
              <ArrowLeft className="w-4 h-4" />
              Back
            </Button>
          )}

          {availableButtonSlugs.includes('swap') && (
            <Button className="flex items-center gap-2">
              <SwapHorizontal className="w-4 h-4" />
              Swap
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}
