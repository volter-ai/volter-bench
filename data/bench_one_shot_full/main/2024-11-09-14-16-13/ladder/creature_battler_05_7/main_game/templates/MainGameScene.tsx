import { useCurrentButtons } from "@/lib/useChoices.ts"
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
  description: string
  stats: {
    hp: number
    max_hp: number
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

  if (!playerCreature || !botCreature) {
    return <div className="h-screen w-screen aspect-video bg-slate-800 flex items-center justify-center">
      <p className="text-white">Loading battle...</p>
    </div>
  }

  const availableSkills = playerCreature.collections.skills.filter(skill => 
    availableButtonSlugs.includes(`skill_${skill.uid}`)
  )

  return (
    <div className="h-screen w-screen aspect-video bg-slate-800 flex flex-col">
      {/* Battlefield Area */}
      <div className="h-2/3 grid grid-cols-2 gap-4 p-4">
        {/* Top Left - Bot Status */}
        <div className="flex items-start justify-start">
          <CreatureCard
            uid={botCreature.uid}
            name={botCreature.display_name}
            image={`/assets/creatures/${botCreature.meta.prototype_id}_front.png`}
            currentHp={botCreature.stats.hp}
            maxHp={botCreature.stats.max_hp}
          />
        </div>

        {/* Top Right - Bot Creature */}
        <div className="flex items-center justify-center relative">
          <div className="absolute bottom-0 w-32 h-4 bg-slate-700 rounded-full opacity-50" />
          <img 
            src={`/assets/creatures/${botCreature.meta.prototype_id}_front.png`}
            alt={botCreature.display_name}
            className="w-32 h-32 object-contain mb-2"
          />
        </div>

        {/* Bottom Left - Player Creature */}
        <div className="flex items-center justify-center relative">
          <div className="absolute bottom-0 w-32 h-4 bg-slate-700 rounded-full opacity-50" />
          <img 
            src={`/assets/creatures/${playerCreature.meta.prototype_id}_back.png`}
            alt={playerCreature.display_name}
            className="w-32 h-32 object-contain mb-2"
          />
        </div>

        {/* Bottom Right - Player Status */}
        <div className="flex items-end justify-end">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            image={`/assets/creatures/${playerCreature.meta.prototype_id}_back.png`}
            currentHp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
          />
        </div>
      </div>

      {/* UI Area */}
      <div className="h-1/3 bg-slate-700 p-4">
        <div className="grid grid-cols-2 gap-4 h-full">
          {availableSkills.map((skill) => (
            <SkillButton
              key={`skill_${skill.uid}`}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={{
                damage: skill.stats.base_damage,
                accuracy: 100,
                type: skill.meta.skill_type
              }}
              onClick={() => emitButtonClick(`skill_${skill.uid}`)}
            />
          ))}
          
          {availableButtonSlugs.includes('back') && (
            <Button 
              key="back"
              onClick={() => emitButtonClick('back')}
              className="flex items-center justify-center gap-2"
            >
              <ArrowLeft className="w-4 h-4" /> Back
            </Button>
          )}
          
          {availableButtonSlugs.includes('swap') && (
            <Button
              key="swap"
              onClick={() => emitButtonClick('swap')}
              className="flex items-center justify-center gap-2"
            >
              <Repeat className="w-4 h-4" /> Swap
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}
