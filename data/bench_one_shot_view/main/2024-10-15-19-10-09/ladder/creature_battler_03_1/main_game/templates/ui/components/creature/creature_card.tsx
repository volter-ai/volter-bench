import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import { Card as ShadcnCard, CardHeader as ShadcnCardHeader, CardTitle as ShadcnCardTitle, CardContent as ShadcnCardContent } from "@/components/ui/card"

let CreatureCard = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & { uid: string; name: string; image: string; hp: number }
>(({ className, uid, name, image, hp, ...props }, ref) => (
  <ShadcnCard ref={ref} className={cn("w-64", className)} uid={uid} {...props}>
    <ShadcnCardHeader>
      <ShadcnCardTitle>{name}</ShadcnCardTitle>
    </ShadcnCardHeader>
    <ShadcnCardContent>
      <img src={image} alt={name} className="w-full h-40 object-cover mb-4" />
      <div>HP: {hp}</div>
    </ShadcnCardContent>
  </ShadcnCard>
))

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
