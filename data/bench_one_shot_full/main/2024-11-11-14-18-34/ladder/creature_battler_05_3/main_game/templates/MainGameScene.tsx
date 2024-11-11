import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, Repeat } from 'lucide-react'
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
    skill_type: string
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

  const playerCreature = props.data?.entities?.player?.entities?.active_creature
  const botCreature = props.data?.entities?.bot?.entities?.active_creature

  if (!props.data?.entities?.player || !props.data?.entities?.bot) {
    return <div className="h-screen w-screen flex items-center justify-center">Loading...</div>
  }

  return (
    <div className="h-screen w-screen aspect-[16/9] relative flex flex-col bg-gradient-to-b from-sky-400 to-sky-200">
      {/* Battlefield Area */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 relative">
        {/* Top Left - Bot Status */}
        <div className="flex items-start justify-end p-4">
          {botCreature && (
            <CreatureCard
              uid={botCreature.uid}
              name={botCreature.display_name}
              hp={botCreature.stats.hp}
              maxHp={botCreature.stats.max_hp}
              imageUrl="/placeholder-creature.png"
              className="scale-75 origin-top-right"
            />
          )}
        </div>

        {/* Top Right - Bot Creature */}
        <div className="flex items-center justify-center p-4">
          {botCreature && (
            <div className="relative">
              <div className="absolute bottom-0 w-32 h-8 bg-black/20 rounded-full blur-sm" />
              <div className="relative">
                {/* Creature image would be here in real implementation */}
                <div className="w-32 h-32 bg-slate-300 rounded-lg" />
              </div>
            </div>
          )}
        </div>

        {/* Bottom Left - Player Creature */}
        <div className="flex items-center justify-center p-4">
          {playerCreature && (
            <div className="relative">
              <div className="absolute bottom-0 w-32 h-8 bg-black/20 rounded-full blur-sm" />
              <div className="relative">
                {/* Creature image would be here in real implementation */}
                <div className="w-32 h-32 bg-slate-300 rounded-lg" />
              </div>
            </div>
          )}
        </div>

        {/* Bottom Right - Player Status */}
        <div className="flex items-end justify-start p-4">
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              hp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
              imageUrl="/placeholder-creature.png"
              className="scale-75 origin-bottom-left"
            />
          )}
        </div>
      </div>

      {/* UI Area */}
      <div className="h-1/3 bg-slate-800/90 p-6">
        <div className="h-full grid grid-cols-2 grid-rows-2 gap-4">
          {availableButtonSlugs.includes('attack') && playerCreature?.collections?.skills?.map((skill, index) => (
            index < 4 && (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={{
                  damage: skill.stats.base_damage,
                  type: skill.meta.skill_type
                }}
                className="w-full h-full"
              />
            )
          ))}
          
          {availableButtonSlugs.includes('back') && (
            <Button
              onClick={() => emitButtonClick('back')}
              className="w-full h-full flex items-center justify-center gap-2"
            >
              <ArrowLeft className="w-6 h-6" />
              Back
            </Button>
          )}
          
          {availableButtonSlugs.includes('swap') && (
            <Button
              onClick={() => emitButtonClick('swap')}
              className="w-full h-full flex items-center justify-center gap-2"
            >
              <Repeat className="w-6 h-6" />
              Swap
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}
