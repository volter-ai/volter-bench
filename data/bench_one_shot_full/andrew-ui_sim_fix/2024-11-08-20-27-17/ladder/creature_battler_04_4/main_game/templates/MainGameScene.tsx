import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Heart, Sword, Shield, Zap } from 'lucide-react';
import { Card } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";

interface ExamplePlayer {
    uid: string;
    stats: {
        stat1: number;
    };
}

interface Creature {
    uid: string;
    display_name: string;
    description: string;
    stats: {
        hp: number;
        max_hp: number;
        attack: number;
        defense: number;
        sp_attack: number;
        sp_defense: number;
        speed: number;
    };
    meta: {
        creature_type: string;
    };
    collections: {
        skills: Skill[];
    };
}

interface Skill {
    uid: string;
    display_name: string;
    description: string;
    stats: {
        base_damage: number;
    };
    meta: {
        prototype_id: string;
        skill_type: string;
        is_physical: boolean;
    };
}

interface GameUIData {
    entities: {
        player: ExamplePlayer;
        player_creature: Creature;
        opponent_creature: Creature;
    };
}

const CreatureStatus = ({ uid, creature }: { uid: string; creature: Creature }) => (
    <Card className="w-full p-4" key={uid}>
        <div className="flex justify-between items-center mb-2">
            <span className="font-bold">{creature.display_name}</span>
            <span className="text-sm">
                {creature.stats.hp}/{creature.stats.max_hp} HP
            </span>
        </div>
        <Progress 
            value={(creature.stats.hp / creature.stats.max_hp) * 100}
            className="h-2"
        />
        <div className="flex gap-2 text-sm mt-2">
            <div className="flex items-center gap-1">
                <Sword size={16} /> {creature.stats.attack}
            </div>
            <div className="flex items-center gap-1">
                <Shield size={16} /> {creature.stats.defense}
            </div>
            <div className="flex items-center gap-1">
                <Zap size={16} /> {creature.stats.speed}
            </div>
        </div>
    </Card>
);

export function MainGameSceneView(props: { data: GameUIData }) {
    const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

    const playerCreature = props.data.entities.player_creature;
    const opponentCreature = props.data.entities.opponent_creature;

    if (!playerCreature || !opponentCreature) return null;

    const SKILL_BUTTONS = ['lick', 'tackle'];

    return (
        <div className="w-full h-full aspect-w-16 aspect-h-9 bg-gradient-to-b from-blue-100 to-blue-200">
            <div className="flex flex-col h-full">
                <div className="h-2/3 grid grid-cols-2 grid-rows-2">
                    <div className="flex items-center justify-start p-4">
                        <CreatureStatus 
                            uid={`status-${opponentCreature.uid}`} 
                            creature={opponentCreature} 
                        />
                    </div>
                    <div className="flex items-center justify-center">
                        <Card className="relative h-32 w-32">
                            <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full blur-sm" />
                            {/* Opponent creature image placeholder */}
                        </Card>
                    </div>
                    <div className="flex items-center justify-center">
                        <Card className="relative h-32 w-32">
                            <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full blur-sm" />
                            {/* Player creature image placeholder */}
                        </Card>
                    </div>
                    <div className="flex items-center justify-end p-4">
                        <CreatureStatus 
                            uid={`status-${playerCreature.uid}`} 
                            creature={playerCreature} 
                        />
                    </div>
                </div>

                <Card className="h-1/3 bg-white/80 p-4">
                    <div className="grid grid-cols-2 gap-4 h-full">
                        {playerCreature.collections.skills
                            .filter(skill => 
                                SKILL_BUTTONS.includes(skill.meta.prototype_id) && 
                                availableButtonSlugs.includes(skill.meta.prototype_id)
                            )
                            .map((skill) => (
                                <Card
                                    key={skill.uid}
                                    className="p-4 hover:bg-slate-100 cursor-pointer"
                                    onClick={() => emitButtonClick(skill.meta.prototype_id)}
                                >
                                    <h3 className="font-bold">{skill.display_name}</h3>
                                    <p className="text-sm">{skill.description}</p>
                                </Card>
                            ))
                        }
                    </div>
                </Card>
            </div>
        </div>
    );
}
