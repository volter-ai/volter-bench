import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import { Card as ShadcnCard, CardHeader, CardContent, CardFooter } from "@/components/ui/card"

interface CreatureCardProps extends React.ComponentPropsWithoutRef<typeof ShadcnCard> {
  uid: string;
  name: string;
  image: string;
  hp: number;
  maxHp: number;
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, image, hp, maxHp, ...props }, ref) => (
    <ShadcnCard ref={ref} className={cn("w-64", className)} uid={uid} {...props}>
      <CardHeader>
        <h3 className="text-lg font-semibold">{name}</h3>
      </CardHeader>
      <CardContent>
        <img src={image} alt={name} className="w-full h-40 object-cover mb-4" />
        <div className="flex justify-between items-center">
          <span>HP:</span>
          <span>{hp}/{maxHp}</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2.5 mt-2">
          <div
            className="bg-green-600 h-2.5 rounded-full"
            style={{ width: `${(hp / maxHp) * 100}%` }}
          ></div>
        </div>
      </CardContent>
    </ShadcnCard>
  )
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
