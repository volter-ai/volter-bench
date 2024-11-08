import { useCurrentButtons } from "@/lib/useChoices.ts"
import { ArrowLeft, SwapHorizontal } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { PlayerCard } from "@/components/ui/custom/player/player_card"
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
    skill_type: string
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
  meta: {
    prototype_id: string
  }
}

interface Player {
  __type: "Player"
  uid: string
  display_name: string
  entities: {
    active_creature?: Creature
  }
  meta: {
    prototype_id: string
  }
}

interface GameUIData {
  entities: {
    player: Player
    bot: Player
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons()

  const playerCreature = props.data.entities.player?.entities.active_creature
  const botCreature = props.data.entities.bot?.entities.active_creature

  if (!playerCreature || !botCreature) {
    return <div className="h-screen w-screen flex items-center justify-center">
      Loading battle...
    </div>
  }

  return (
    <div className="h-screen w-screen flex flex-col bg-slate-900">
      {/* Battlefield Area */}
      <div className="h-2/3 grid grid-cols-2 gap-4 p-4">
        {/* Top Left - Bot Status */}
        <div className="flex justify-start items-start">
          <CreatureCard
            uid={botCreature.uid}
            name={botCreature.display_name}
            imageUrl={`/assets/creatures/${botCreature.meta.prototype_id}_front.png`}
            currentHp={botCreature.stats.hp}
            maxHp={botCreature.stats.max_hp}
          />
        </div>

        {/* Top Right - Bot Creature */}
        <div className="flex justify-end items-start">
          <PlayerCard
            uid={props.data.entities.bot.uid}
            name={props.data.entities.bot.display_name}
            imageUrl={`/assets/players/${props.data.entities.bot.meta.prototype_id}.png`}
          />
        </div>

        {/* Bottom Left - Player Creature */}
        <div className="flex justify-start items-end">
          <PlayerCard
            uid={props.data.entities.player.uid}
            name={props.data.entities.player.display_name}
            imageUrl={`/assets/players/${props.data.entities.player.meta.prototype_id}.png`}
          />
        </div>

        {/* Bottom Right - Player Status */}
        <div className="flex justify-end items-end">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            imageUrl={`/assets/creatures/${playerCreature.meta.prototype_id}_back.png`}
            currentHp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
          />
        </div>
      </div>

      {/* UI Area */}
      <div className="h-1/3 bg-slate-800">
        <div className="h-full grid grid-cols-2 grid-rows-2 gap-4 p-4">
          {availableButtonSlugs.includes('attack') && playerCreature.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={{
                damage: skill.stats.base_damage,
                type: skill.meta.skill_type
              }}
              onClick={() => emitButtonClick('attack', { skillId: skill.uid })}
            />
          ))}
          
          {availableButtonSlugs.includes('back') && (
            <Button 
              className="flex items-center gap-2"
              onClick={() => emitButtonClick('back')}
            >
              <ArrowLeft className="w-4 h-4" /> Back
            </Button>
          )}
          
          {availableButtonSlugs.includes('swap') && (
            <Button 
              className="flex items-center gap-2"
              onClick={() => emitButtonClick('swap')}
            >
              <SwapHorizontal className="w-4 h-4" /> Swap
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}
