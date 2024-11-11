import { useCurrentButtons } from "@/lib/useChoices.ts";
import { ArrowLeft, SwapHorizontal } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"
import { CreatureDisplay } from "@/components/ui/custom/creature/creature_display"
import { Button } from "@/components/ui/button"

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

  const playerCreature = props.data.entities.player?.entities.active_creature
  const botCreature = props.data.entities.bot?.entities.active_creature

  return (
    <div className="h-screen w-screen aspect-[16/9] bg-slate-900 flex flex-col">
      {/* Battlefield Area */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Top Left - Bot Status */}
        <div className="flex justify-start items-start">
          {botCreature && botCreature.__type === "Creature" && (
            <CreatureCard
              uid={botCreature.uid}
              name={botCreature.display_name}
              image="/placeholder.png"
              currentHp={botCreature.stats.hp}
              maxHp={botCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Top Right - Bot Creature */}
        <div className="flex justify-end items-start">
          {botCreature && botCreature.__type === "Creature" && (
            <CreatureDisplay
              uid={botCreature.uid}
              name={botCreature.display_name}
              image="/placeholder.png"
              isFront={true}
            />
          )}
        </div>

        {/* Bottom Left - Player Creature */}
        <div className="flex justify-start items-end">
          {playerCreature && playerCreature.__type === "Creature" && (
            <CreatureDisplay
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              image="/placeholder.png"
              isFront={false}
            />
          )}
        </div>

        {/* Bottom Right - Player Status */}
        <div className="flex justify-end items-end">
          {playerCreature && playerCreature.__type === "Creature" && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              image="/placeholder.png"
              currentHp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>
      </div>

      {/* UI Area */}
      <div className="h-1/3 p-4">
        <div className="grid grid-cols-2 gap-4 h-full">
          {availableButtonSlugs.includes('attack') && playerCreature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              name={skill.display_name}
              description={skill.description}
              stats={{ damage: skill.stats.base_damage }}
              onClick={() => emitButtonClick('attack', { skill_uid: skill.uid })}
            />
          ))}
          
          {availableButtonSlugs.includes('back') && (
            <Button
              onClick={() => emitButtonClick('back')}
              className="w-full h-full"
            >
              <ArrowLeft className="mr-2" />
              Back
            </Button>
          )}
          
          {availableButtonSlugs.includes('swap') && (
            <Button
              onClick={() => emitButtonClick('swap')}
              className="w-full h-full"
            >
              <SwapHorizontal className="mr-2" />
              Swap Creature
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}
