import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Sword, Droplet, Flame } from 'lucide-react';

interface Skill {
    uid: string;
    display_name: string;
    description: string;
    meta: {
        skill_type: string;
        prototype_id: string;
    };
    stats: {
        base_damage: number;
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
        prototype_id: string;
        creature_type: string;
    };
    collections: {
        skills: Skill[];
    };
}

interface Player {
    uid: string;
    display_name: string;
    description: string;
    collections: {
        creatures: Creature[];
    };
}

interface GameUIData {
    entities: {
        player: Player;
        opponent: Player;
        player_creature: Creature;
        opponent_creature: Creature;
    };
}

const CreatureStatus = ({ creature, uid }: { creature: Creature; uid: string }) => {
    const hpPercentage = (creature.stats.hp / creature.stats.max_hp) * 100;
    
    return (
        <Card key={uid} className="p-4 w-48">
            <h3 className="font-bold">{creature.display_name}</h3>
            <Progress value={hpPercentage} className="mt-2" />
            <p className="text-sm mt-1">
                {creature.stats.hp} / {creature.stats.max_hp} HP
            </p>
        </Card>
    );
};

const CreatureDisplay = ({ creature, isPlayer, uid }: { creature: Creature; isPlayer: boolean; uid: string }) => {
    const TypeIcon = creature.meta.creature_type === 'water' ? Droplet : Flame;
    
    return (
        <div key={uid} className="relative flex flex-col items-center">
            <div className="w-32 h-32 bg-black/10 rounded-full absolute bottom-0" />
            <div className="mb-4">
                <TypeIcon className={`w-16 h-16 ${isPlayer ? 'transform rotate-180' : ''}`} />
            </div>
        </div>
    );
};

export function MainGameSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons();

    const { player_creature, opponent_creature } = props.data.entities;

    if (!player_creature || !opponent_creature) {
        return <div>Loading battle...</div>;
    }

    return (
        <div className="w-full h-full aspect-w-16 aspect-h-9 bg-gradient-to-b from-blue-100 to-blue-200">
            {/* Battlefield Area */}
            <div className="h-2/3 grid grid-cols-2 gap-4 p-4">
                {/* Opponent Status */}
                <div className="flex items-start justify-start">
                    <CreatureStatus 
                        creature={opponent_creature} 
                        uid={`status-${opponent_creature.uid}`}
                    />
                </div>
                
                {/* Opponent Creature */}
                <div className="flex items-center justify-center">
                    <CreatureDisplay 
                        creature={opponent_creature}
                        isPlayer={false}
                        uid={`display-${opponent_creature.uid}`}
                    />
                </div>
                
                {/* Player Creature */}
                <div className="flex items-end justify-center">
                    <CreatureDisplay 
                        creature={player_creature}
                        isPlayer={true}
                        uid={`display-${player_creature.uid}`}
                    />
                </div>
                
                {/* Player Status */}
                <div className="flex items-end justify-end">
                    <CreatureStatus 
                        creature={player_creature}
                        uid={`status-${player_creature.uid}`}
                    />
                </div>
            </div>

            {/* Battle Controls */}
            <Card className="h-1/3 p-4">
                <div className="grid grid-cols-2 gap-4 h-full">
                    {availableButtonSlugs?.map((buttonId) => (
                        <Button
                            key={buttonId}
                            onClick={() => emitButtonClick(buttonId)}
                            variant="default"
                            className="flex items-center justify-center gap-2"
                        >
                            <Sword className="w-5 h-5" />
                            {buttonId.charAt(0).toUpperCase() + buttonId.slice(1)}
                        </Button>
                    ))}
                </div>
            </Card>
        </div>
    );
}
